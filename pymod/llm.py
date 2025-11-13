# modules/llm_enrichment.py
"""
Robust enrichment module using MakerSuite google.generativeai.
Tries multiple SDK call shapes (chat.create, models.generate, GenerativeModel, etc.)
and falls back to a local rewriter if Gemini fails.
"""

import os
import inspect
from typing import List
from .utils import chunk_text_by_chars

# Try to import MakerSuite SDK
try:
    import google.generativeai as genai
    GENAI_PKG = True
except Exception:
    genai = None
    GENAI_PKG = False


def _extract_text_from_response(resp) -> str:
    """Try to extract plain text from a variety of response shapes."""
    try:
        # many shapes have .text
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()
    except Exception:
        pass

    try:
        # older shapes: resp.candidates[0].content.parts[0].text or resp.candidates[0].content[0]['text']
        candidates = getattr(resp, "candidates", None)
        if candidates:
            c0 = candidates[0]
            # try attribute access
            if hasattr(c0, "content"):
                cont = c0.content
                # cont might be object with parts or list
                if isinstance(cont, list) and cont:
                    first = cont[0]
                    if hasattr(first, "text"):
                        return first.text.strip()
                    if isinstance(first, dict) and "text" in first:
                        return first["text"].strip()
                if hasattr(cont, "parts"):
                    parts = getattr(cont, "parts", None)
                    if isinstance(parts, list) and parts:
                        p0 = parts[0]
                        if hasattr(p0, "text"):
                            return p0.text.strip()
    except Exception:
        pass

    try:
        # some responses have .output with content list
        out = getattr(resp, "output", None)
        if out and isinstance(out, list):
            c0 = out[0]
            if isinstance(c0, dict) and "content" in c0:
                cont = c0["content"]
                if isinstance(cont, list) and cont:
                    first = cont[0]
                    if isinstance(first, dict) and "text" in first:
                        return first["text"].strip()
    except Exception:
        pass

    # fallback to string conversion
    try:
        return str(resp)
    except Exception:
        return "<no-text-extracted>"


def _try_call(callable_obj, prompt: str, chosen_model: str, temperature: float, allow_messages: bool = True):
    """
    Signature-aware caller for different SDK methods. Returns response or raises an exception.
    """
    last_err = None

    # 1) try simple positional call: method(prompt)
    try:
        return callable_obj(prompt)
    except TypeError as e:
        last_err = e
    except Exception as e:
        last_err = e

    # 2) try named arg patterns
    attempts = [
        {"prompt": prompt, "temperature": temperature},
        {"input": prompt, "temperature": temperature},
        {"text": prompt, "temperature": temperature},
        {"messages": [{"role": "user", "content": prompt}], "temperature": temperature},
        {"messages": [{"role": "system", "content": "You are an audiobook copywriter."},
                      {"role": "user", "content": prompt}], "temperature": temperature},
    ]
    for kwargs in attempts:
        # don't try messages if disallowed
        if "messages" in kwargs and not allow_messages:
            continue
        try:
            # many methods accept model param too
            try:
                return callable_obj(model=chosen_model, **kwargs)
            except TypeError:
                return callable_obj(**kwargs)
        except TypeError as e:
            last_err = e
        except Exception as e:
            last_err = e

    # 3) try passing a single-element contents list if method name suggests it (for some shapes)
    try:
        return callable_obj(chosen_model, [prompt])
    except Exception as e:
        last_err = e

    # 4) no more attempts
    raise last_err if last_err is not None else RuntimeError("Could not call method")


def gemini_rewrite_chunks(chunks: List[str], model: str = None, temperature: float = 0.6) -> List[str]:
    """
    Robust rewrite using MakerSuite `google.generativeai` package.
    Tries multiple call shapes and returns rewritten chunks.
    If all Gemini attempts fail for a chunk, falls back to local rewriter for that chunk.
    """
    chosen_model = model or os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
    rewritten = []

    if not GENAI_PKG:
        # no SDK installed: fall back on local rewriter for everything
        for c in chunks:
            rewritten.append(fallback_rewrite(c))
        return rewritten

    # configure with API key if available
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is required in environment.")

    try:
        genai.configure(api_key=api_key)
    except Exception:
        # ignore if configure not present
        pass

    for chunk in chunks:
        prompt = (
            "Rewrite the following passage for an engaging audiobook narration. "
            "Remove underscores, hyphenation across lines, and extraneous formatting. "
            "Keep the meaning identical and break into short sentences/paragraphs appropriate for narration.\n\n"
            + chunk
        )

        last_exc = None
        # Try several preferred call patterns in order

        # Pattern A: genai.chat.create(...)
        try:
            chat_api = getattr(genai, "chat", None)
            if chat_api and hasattr(chat_api, "create"):
                try:
                    resp = chat_api.create(
                        model=chosen_model,
                        messages=[
                            {"role": "system", "content": "You are an audiobook copywriter."},
                            {"role": "user", "content": prompt}
                        ],
                    )
                    rewritten.append(_extract_text_from_response(resp))
                    continue
                except Exception as e:
                    last_exc = e
        except Exception as e:
            last_exc = e

        # Pattern B: genai.models.generate(...) or genai.models.generate_text(...)
        try:
            models_api = getattr(genai, "models", None)
            if models_api:
                if hasattr(models_api, "generate"):
                    try:
                        resp = genai.models.generate(model=chosen_model, input=prompt)
                        rewritten.append(_extract_text_from_response(resp))
                        continue
                    except Exception as e:
                        last_exc = e
                if hasattr(models_api, "generate_text"):
                    try:
                        resp = genai.models.generate_text(model=chosen_model, input=prompt)
                        rewritten.append(_extract_text_from_response(resp))
                        continue
                    except Exception as e:
                        last_exc = e
        except Exception as e:
            last_exc = e

        # Pattern C: top-level convenience functions (generate_text / generate)
        try:
            if hasattr(genai, "generate_text"):
                try:
                    resp = genai.generate_text(model=chosen_model, prompt=prompt)
                    rewritten.append(_extract_text_from_response(resp))
                    continue
                except Exception as e:
                    last_exc = e
            if hasattr(genai, "generate"):
                try:
                    resp = genai.generate(model=chosen_model, prompt=prompt)
                    rewritten.append(_extract_text_from_response(resp))
                    continue
                except Exception as e:
                    last_exc = e
        except Exception as e:
            last_exc = e

        # Pattern D: GenerativeModel class (older versions)
        try:
            if hasattr(genai, "GenerativeModel"):
                try:
                    ModelCls = getattr(genai, "GenerativeModel")
                    model_obj = ModelCls(chosen_model)
                    # try common instance methods
                    for name in ("generate", "generate_text", "generate_content", "generate_response", "create"):
                        if hasattr(model_obj, name):
                            method = getattr(model_obj, name)
                            try:
                                resp = _try_call(method, prompt, chosen_model, temperature, allow_messages=False)
                                rewritten.append(_extract_text_from_response(resp))
                                raise StopIteration  # success
                            except StopIteration:
                                break
                            except Exception as e:
                                last_exc = e
                                continue
                except StopIteration:
                    continue
                except Exception as e:
                    last_exc = e
        except Exception as e:
            last_exc = e

        # If we reach here, none of the Gemini patterns succeeded for this chunk.
        # Use local fallback rewrite (cleaned) so audio still reads well — do not use raw extracted text.
        try:
            rewritten_chunk = fallback_rewrite(chunk)
            rewritten.append(rewritten_chunk)
        except Exception:
            # ultimate fallback: minimal safe text
            rewritten.append(" ")  # produce blank short audio rather than dump raw messy text

    return rewritten


def fallback_rewrite(chunk: str) -> str:
    """
    Conservative local rewriter that removes weird characters, hyphenations,
    collapses whitespace, and keeps only readable sentences for TTS.
    """
    import re
    s = chunk or ""
    # fix hyphenation across lines: "exam-\nple" -> "example"
    s = re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '', s)
    # replace underscores and long dashes with space
    s = s.replace('_', ' ').replace('—', ' ').replace('–', ' ')
    # remove unusual non-printable characters
    s = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', s)
    # remove bracketed short tokens like [1], (2)
    s = re.sub(r'\[\s*\w{1,10}\s*\]',' ', s)
    s = re.sub(r'\(\s*\d{1,4}\s*\)',' ', s)
    # collapse whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    # ensure sentences separated reasonably
    s = re.sub(r'\s*([.!?])\s*', r'\1 ', s)
    # if still very long without punctuation, insert pauses
    if len(s) > 1200 and '.' not in s[:800]:
        s = '. '.join([s[i:i+700].strip() for i in range(0, len(s), 700)])
    return s.strip()


def enrich_text(text: str, use_gemini: bool = True) -> str:
    """
    Top-level wrapper called by app.
    If use_gemini=True, try Gemini for rewriting; on Gemini failure for a chunk, fallback_rewrite is used.
    """
    if not text:
        return ""

    chunks = chunk_text_by_chars(text, max_chars=2500)
    if use_gemini:
        return "\n\n".join(gemini_rewrite_chunks(chunks))
    else:
        return "\n\n".join([fallback_rewrite(c) for c in chunks])
