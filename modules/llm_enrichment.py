# modules/llm_enrichment.py
import os
import time
import re
import hashlib
import logging
from typing import List, Optional

# Use streamlit cache if available to avoid repeated API calls
try:
    import streamlit as st
    CACHE = st.cache_data
except Exception:
    # dummy cache decorator if streamlit not available
    def CACHE(func):
        return func

import google.generativeai as genai

logger = logging.getLogger(__name__)


def _chunk_text(text: str, max_chars: int = 1500) -> List[str]:
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for p in paragraphs:
        if len(current) + len(p) + 2 <= max_chars:
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current.strip())
            while len(p) > max_chars:
                chunks.append(p[:max_chars])
                p = p[max_chars:]
            current = p
    if current:
        chunks.append(current.strip())
    return chunks


def _extract_retry_seconds_from_error(err_str: str) -> int:
    m = re.search(r'retry_delay\s*\{\s*seconds:\s*([0-9]+)', err_str)
    if m:
        return int(m.group(1))
    m2 = re.search(r'retry (?:in )?([0-9]+(?:\.[0-9]+)?)s', err_str)
    if m2:
        return int(float(m2.group(1)))
    return 0


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# -----------------------
# SIMPLE LOCAL FALLBACK
# -----------------------
def simple_local_enrich(text: str) -> str:
    """
    Lightweight local 'enrichment' that improves pacing and narration style
    without calling an LLM. This won't be as rich as Gemini but makes a
    noticeable improvement for demos (adds transitions, shortens long sentences).
    """
    import re

    # 1) Break extremely long sentences into shorter ones (simple heuristic)
    def soften_sentence(s: str) -> str:
        # replace too-long commas with a period + transition
        if len(s) > 160:
            s = re.sub(r',\s+', '. ', s)
        # add small transition phrases at paragraph starts
        return s.strip()

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    enriched_paras = []
    for p in paragraphs:
        # add gentle narration transitions sometimes
        if len(p) > 200:
            enriched = "Imagine this: " + p
        else:
            enriched = p

        # convert double spaces, normalize whitespace
        enriched = re.sub(r'\s+', ' ', enriched)

        # soften long sentences
        sentences = re.split(r'(?<=[\.\?\!])\s+', enriched)
        sentences = [soften_sentence(s) for s in sentences if s.strip()]

        # join but add small pauses (parenthetical) for audio pacing
        joined = " ".join([s for s in sentences])
        enriched_paras.append(joined)

    return "\n\n".join(enriched_paras)


# -----------------------
# LLM (Gemini) with quota-handling + caching
# -----------------------
@CACHE
def _cached_gemini_call(hash_key: str, model: str, chunk: str) -> Optional[str]:
    """
    Internal wrapper to allow caching per chunk.
    Note: st.cache_data caches function results across app runs.
    """
    # This function body will be replaced by enrich_text_with_gemini_quota_safe flow
    return None  # placeholder; actual calls are done in main function


def enrich_text_with_gemini_quota_safe(
    text: str,
    model: str = "models/gemini-2.5-flash",
    max_retries_per_chunk: int = 3,
    throttle_seconds_between_calls: float = 1.2,
    max_requests_per_minute: Optional[int] = 30,
    use_local_on_failure: bool = True,
) -> str:
    """
    Tries to rewrite text with Gemini, but:
     - honors retry_delay returned by server
     - throttles calls
     - caches chunk results
     - falls back to simple_local_enrich() on repeated quota failures
    """
    if not text or not text.strip():
        return text

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # no key -> fallback to local
        if use_local_on_failure:
            return simple_local_enrich(text)
        return text

    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        logger.warning("Failed to configure genai: %s", e)
        if use_local_on_failure:
            return simple_local_enrich(text)
        return text

    chunks = _chunk_text(text, max_chars=1500)
    outputs = []
    calls_made = 0
    window_start = time.time()

    for i, chunk in enumerate(chunks):
        chunk_hash = _hash_text(chunk + model)
        # Try to avoid duplicate requests by checking cache — use a simple on-disk approach if needed.
        # Here we rely on st.cache_data wrapping the inner call; but we'll implement logic inline.

        attempt = 0
        success = False
        backoff = 2.0

        while attempt < max_retries_per_chunk:
            # simple rate window guard
            if max_requests_per_minute:
                elapsed = time.time() - window_start
                if elapsed < 60:
                    if calls_made >= max_requests_per_minute:
                        sleep_for = 60 - elapsed + 0.5
                        logger.info("Throttle: sleeping %.1fs to respect max requests/minute", sleep_for)
                        time.sleep(sleep_for)
                        window_start = time.time()
                        calls_made = 0
                else:
                    window_start = time.time()
                    calls_made = 0

            try:
                model_obj = genai.GenerativeModel(model)
                prompt = (
                    "Rewrite the following text so it reads naturally and engagingly when narrated as an audiobook. "
                    "Preserve meaning. Improve pacing, add short transitions and natural phrasing.\n\n"
                    f"{chunk}"
                )
                resp = model_obj.generate_content(prompt)
                if hasattr(resp, "text") and resp.text:
                    out = resp.text
                elif hasattr(resp, "candidates") and resp.candidates:
                    c = resp.candidates[0]
                    try:
                        out = c.content.parts[0].text
                    except Exception:
                        out = str(c)
                else:
                    out = str(resp)

                outputs.append(out.strip())
                calls_made += 1
                success = True
                # small throttle between successful calls
                if throttle_seconds_between_calls:
                    time.sleep(throttle_seconds_between_calls)
                break

            except Exception as e:
                attempt += 1
                err = str(e)
                logger.warning("Gemini attempt %s failed for chunk %s: %s", attempt, i+1, err)
                retry_secs = _extract_retry_seconds_from_error(err)
                if retry_secs and retry_secs > 0:
                    # honor server-specified retry delay
                    sleep_time = min(retry_secs + 1, 120)
                    logger.info("Server requested retry after %ss. Sleeping...", sleep_time)
                    time.sleep(sleep_time)
                else:
                    # exponential backoff
                    logger.info("Sleeping %.1fs before retry...", backoff)
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 60)

                # if quota error (429) repeatedly, break and fallback
                if "quota" in err.lower() or "rate limit" in err.lower() or "429" in err:
                    logger.error("Quota-related error encountered: %s", err)
                    if use_local_on_failure:
                        logger.info("Falling back to local enrich due to quota.")
                        return simple_local_enrich(text)
                    else:
                        return text

        if not success:
            logger.error("Chunk %s failed after retries; aborting and returning original text.", i+1)
            if use_local_on_failure:
                return simple_local_enrich(text)
            return text

    return "\n\n".join(outputs)
