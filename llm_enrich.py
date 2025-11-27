# llm_enrich.py
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def enrich_with_prompt(text, max_len_chars=20000):
    """
    If OPENAI_API_KEY is present, send text to OpenAI to rewrite in audiobook narration style.
    If no key, return the original text.
    Note: We chunk to avoid massive requests.
    """
    if not OPENAI_KEY:
        return text

    import openai
    openai.api_key = OPENAI_KEY

    # Simple prompt
    prompt = (
        "Rewrite the following text into an engaging audiobook narration style. "
        "Keep meaning, but produce flowing, listener-friendly narration. "
        "Keep sections short and natural for speech. "
    )

    # If text is too long, just ask for the whole summary rewrite in chunks outside (app will chunk).
    messages = [
        {"role":"system","content":"You are an assistant that rewrites prose into audiobook narration style."},
        {"role":"user","content": prompt + "\n\n" + text}
    ]
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini", # model choice; if unavailable, openai will raise
            messages=messages,
            temperature=0.7,
            max_tokens=2500
        )
        return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        # Fail gracefully and return original text
        print("LLM enrich failed:", e)
        return text