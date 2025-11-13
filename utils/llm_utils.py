"""
Helpers for summarization.
Supports OpenAI (ChatCompletion) and a fallback local transformers pipeline.
"""

import os
from typing import Optional

# Try imports only when needed to avoid heavy startup cost
def llm_available_openai() -> bool:
    try:
        import importlib.util
        return importlib.util.find_spec("openai") is not None
    except Exception:
        return False

def llm_available_transformers() -> bool:
    try:
        import importlib.util
        return importlib.util.find_spec("transformers") is not None
    except Exception:
        return False

# ---------------- OpenAI summarization ----------------
def summarize_with_openai(text: str, api_key: str, max_words: int = 150) -> str:
    """
    Summarize using OpenAI chat completion (gpt-3.5-turbo).
    Requires `openai` package and a valid API key.
    """
    import openai
    openai.api_key = api_key

    prompt = (
        "You are a helpful assistant that produces a concise summary. "
        f"Produce a summary of the following text in approximately {max_words} words. "
        "Keep it clear and organized.\n\n"
        f"TEXT:\n\n{text}"
    )

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2,
        max_tokens= max(200, int(max_words * 6))  # approx tokens
    )
    summary = resp["choices"][0]["message"]["content"].strip()
    return summary

# ---------------- Local transformers summarization ----------------
def summarize_with_transformers(text: str, max_words: int = 150, model_name: str = "sshleifer/distilbart-cnn-12-6") -> str:
    """
    Use HuggingFace transformers summarization pipeline (smaller model by default).
    Requires `transformers` and a torch backend. May be slow on CPU.
    """
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

    # load model & pipeline
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    # chunk if text is large
    max_chunk = 1000  # approx tokens per chunk
    sentences = text.split(". ")
    chunks = []
    cur = ""
    for s in sentences:
        if len(cur) + len(s) < max_chunk:
            cur += s + ". "
        else:
            chunks.append(cur.strip())
            cur = s + ". "
    if cur:
        chunks.append(cur.strip())

    summaries = []
    for c in chunks:
        out = summarizer(c, max_length=int(max_words*1.5), min_length=30, do_sample=False)
        summaries.append(out[0]["summary_text"])
    combined = " ".join(summaries)
    return combined
