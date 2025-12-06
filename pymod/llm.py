# modules/llm_enrichment.py
"""
Robust MakerSuite-compatible enrichment module for google-generativeai==0.8.5.

Features:
- Normalizes model names and tries safe fallbacks.
- Tries multiple SDK call shapes (GenerativeModel instance, chat.create, models.generate, top-level generate_text/generate).
- Signature-aware try-calls to avoid invalid kwargs where possible.
- Extracts textual output from many response shapes.
- Exposes enrich_text(text: str, use_gemini: bool=True) -> str
"""

import os
import inspect
from typing import List
from .utils import chunk_text_by_chars

# Attempt import for MakerSuite client
try:
    import google.generativeai as genai
    GEMINI_PKG = True
except Exception:
    genai = None
    GEMINI_PKG = False


def _extract_text_from_gemini_response(resp) -> str:
    """Robustly extract best text candidate from many response shapes."""
    try:
        if hasattr(resp, "text") and resp.text:
            return resp.text if isinstance(resp.text, str) else str(resp.text)
    except Exception:
        pass

    try:
        # candidates -> content -> parts -> text
        cand = getattr(resp, "candidates", None)
        if cand:
            c0 = cand[0]
            # try nested content.parts[0].text
            cont = getattr(c0, "content", None) or (c0.get("content") if isinstance(c0, dict) else None)
            if cont and isinstance(cont, list):
                first = cont[0]
                if isinstance(first, dict) and "text" in first:
                    return first["text"]
                if hasattr(first, "text"):
                    return first.text
            if hasattr(c0, "text") and c0.text:
                return c0.text
    except Exception:
        pass

    try:
        out = getattr(resp, "output", None)
        if out and isinstance(out, list) and out:
            entry = out[0]
            if isinstance(entry, dict) and "content" in entry:
                cont = entry["content"]
                if isinstance(cont, list) and cont and isinstance(cont[0], dict) and "text" in cont[0]:
                    return cont[0]["text"]
    except Exception:
        pass

    try:
        # try mapping-like shapes
        if isinstance(resp, dict):
            # flatten possible paths
            for path in ("output_text", "text"):
                if path in resp and resp[path]:
                    return resp[path]
    except Exception:
        pass

    try:
        return str(resp)
    except Exception:
        return "<no-text-extracted>"


def _try_call(callable_obj, prompt: str, temperature: float = 0.6, allow_messages: bool = True):
    """
    Attempt calling callable_obj in commonly used shapes.
    Returns response object on success, or raises last exception.
    """
    last_exc = None

    # 1) try positional (prompt first)
    try:
        return callable_obj(prompt, temperature=temperature)
    except Exception as e:
        last_exc = e

    # 2) try common named-arg shapes
    named_attempts = [
        {"prompt": prompt, "temperature": temperature, "max_output_tokens": 800},
        {"input": prompt, "temperature": temperature, "max_output_tokens": 800},
        {"text": prompt, "temperature": temperature, "max_output_tokens": 800},
    ]
    for kwargs in named_attempts:
        try:
            return callable_obj(**kwargs)
        except Exception as e:
            last_exc = e

    # 3) messages style (only if allowed)
    if allow_messages:
        try:
            return callable_obj(messages=[{"role": "user", "content": prompt}], temperature=temperature)
        except Exception as e:
            last_exc = e

        # some variants accept messages as first positional arg
        try:
            return callable_obj([{"role": "user", "content": prompt}], temperature=temperature)
        except Exception as e:
            last_exc = e

    # 4) try prompt-only
    try:
        return callable_obj(prompt)
    except Exception as e:
        last_exc = e

    # nothing worked
    raise last_exc if last_exc is not None else RuntimeError("Unable to call callable_obj")


def _normalize_and_choose_models(raw_model: str = None) -> List[str]:
    """
    Normalize raw model string and return a prioritized list of candidate model names to try.
    This prevents malformed names like 'gemini-2.5 Flash' from being used directly.
    """
    candidates = []
    raw = (raw_model or os.environ.get("GEMINI_MODEL") or "").strip()
    if raw:
        normalized = raw.replace(" ", "-").lower()
        candidates.append(normalized)

    # sensible known-good fallbacks (order: preferred -> fallback)
    fallbacks = [
        "gemini-2.1",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5",
        "gemini-1.0"
    ]

    for f in fallbacks:
        if f not in candidates:
            candidates.append(f)

    # ensure unique and return
    seen = set()
    out = []
    for m in candidates:
        if m and m not in seen:
            seen.add(m)
            out.append(m)
    return out


def gemini_rewrite_chunks(chunks: List[str], model: str = None, temperature: float = 0.6) -> List[str]:
    """
    Core function: takes chunk list, calls MakerSuite Gemini using robust fallbacks,
    returns a list of rewritten chunk strings (one per input chunk).
    """
    if not GEMINI_PKG:
        raise RuntimeError("google.generativeai package not installed. Install: pip install google-generativeai==0.8.5")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment. Set it before running.")

    # configure SDK (best-effort)
    try:
        genai.configure(api_key=api_key)
    except Exception:
        # sometimes configure fails silently; continue and rely on call-time auth
        pass

    model_candidates = _normalize_and_choose_models(model)
    rewritten = []
    last_exc_global = None

    for chunk in chunks:
        prompt = (
            "Rewrite the following passage for an engaging audiobook narration. "
            "Fix formatting issues, remove underscores and stray hyphens, ensure natural spoken flow.\n\n"
            + chunk
        )

        chunk_done = False
        last_exc_for_chunk = None

        # try model candidates in order
        for mc in model_candidates:
            # try multiple SDK patterns for this model
            try:
                # 1) GenerativeModel instance path (common in 0.8.x)
                if hasattr(genai, "GenerativeModel"):
                    try:
                        ModelCls = getattr(genai, "GenerativeModel")
                        model_obj = ModelCls(mc)
                        for method_name in ("generate", "generate_text", "generate_content", "create", "generate_response"):
                            if hasattr(model_obj, method_name):
                                method = getattr(model_obj, method_name)
                                allow_messages = method_name not in ("generate_content",)
                                try:
                                    resp = _try_call(method, prompt, temperature=temperature, allow_messages=allow_messages)
                                    text = _extract_text_from_gemini_response(resp)
                                    rewritten.append(text.strip())
                                    chunk_done = True
                                    break
                                except Exception as e:
                                    last_exc_for_chunk = e
                                    continue
                        if chunk_done:
                            break
                    except Exception as e:
                        last_exc_for_chunk = e

                # 2) chat.create fallback
                if hasattr(genai, "chat") and hasattr(genai.chat, "create"):
                    try:
                        resp = genai.chat.create(
                            model=mc,
                            messages=[
                                {"role": "system", "content": "You are an audiobook copywriter."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=temperature
                        )
                    except TypeError:
                        # alternate call shape
                        resp = genai.chat.create([{"role": "user", "content": prompt}], model=mc)
                    text = _extract_text_from_gemini_response(resp)
                    rewritten.append(text.strip())
                    chunk_done = True
                    break
            except Exception as e:
                last_exc_for_chunk = e

            # 3) models.generate / generate_text if available
            try:
                models_api = getattr(genai, "models", None)
                if models_api:
                    if hasattr(models_api, "generate"):
                        resp = genai.models.generate(model=mc, input=prompt)
                        text = _extract_text_from_gemini_response(resp)
                        rewritten.append(text.strip())
                        chunk_done = True
                        break
                    if hasattr(models_api, "generate_text"):
                        resp = genai.models.generate_text(model=mc, input=prompt)
                        text = _extract_text_from_gemini_response(resp)
                        rewritten.append(text.strip())
                        chunk_done = True
                        break
            except Exception as e:
                last_exc_for_chunk = e

            # 4) top-level generate_text / generate
            try:
                if hasattr(genai, "generate_text"):
                    resp = genai.generate_text(model=mc, prompt=prompt)
                    text = _extract_text_from_gemini_response(resp)
                    rewritten.append(text.strip())
                    chunk_done = True
                    break
                if hasattr(genai, "generate"):
                    resp = genai.generate(model=mc, input=prompt)
                    text = _extract_text_from_gemini_response(resp)
                    rewritten.append(text.strip())
                    chunk_done = True
                    break
            except Exception as e:
                last_exc_for_chunk = e

            # if model candidate mc failed, continue to next mc
            if chunk_done:
                break

        # finished trying all models and patterns for this chunk
        if not chunk_done:
            # append informative failure string rather than silently falling back to raw text
            msg = f"[Gemini failed: {repr(last_exc_for_chunk)}]"
            rewritten.append(msg)
            last_exc_global = last_exc_for_chunk

    # raise a global error optionally? For now return what we got (caller can detect failure strings)
    return rewritten


def fallback_rewrite(chunk: str) -> str:
    """Lightweight local rewrite in case Gemini isn't used."""
    import re
    s = re.sub(r'\s+', ' ', chunk.strip())
    s = re.sub(r'[^A-Za-z0-9.,?!\'\" \n]', ' ', s)
    return s.strip()


def enrich_text(text: str, use_gemini: bool = True) -> str:
    """
    Top-level wrapper: splits text into chunks and either calls Gemini or uses fallback rewrite.
    Returns a single string (chunks joined by double-newline).
    """
    chunks = chunk_text_by_chars(text, max_chars=2500)
    if use_gemini:
        if not os.environ.get("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY required in environment to use Gemini.")
        rewritten_chunks = gemini_rewrite_chunks(chunks)
        return "\n\n".join(rewritten_chunks)
    else:
        return "\n\n".join([fallback_rewrite(c) for c in chunks])
