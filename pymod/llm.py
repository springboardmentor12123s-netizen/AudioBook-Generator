import os
import time
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# --------------------------------------------------
# Load .env safely (absolute path)
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

# --------------------------------------------------
# Language prompts (STRICT OUTPUT)
# --------------------------------------------------
LANGUAGE_PROMPTS = {
    "English": "Rewrite the text into clear, natural English.",
    "Hindi": "Rewrite and translate the text into clear, natural Hindi.",
    "Telugu": "Rewrite and translate the text into clear, natural Telugu.",
    "Marathi": "Rewrite and translate the text into clear, natural Marathi.",
    "Odia": "Rewrite and translate the text into clear, natural Odia."
}

def _call_llm(prompt: str) -> str:
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    delay = 2
    last_error = None

    for _ in range(4):
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
            raise RuntimeError("Empty LLM response")

        except Exception as e:
            last_error = e
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"LLM failed: {e}")

    raise RuntimeError(f"LLM unavailable: {last_error}")

def enrich_and_translate_text(text: str, target_language: str, rewrite_only=False) -> str:
    if not text.strip():
        return text

    instruction = (
        "Rewrite the following text for audiobook narration. "
        "Output ONLY the rewritten content. "
        "Do NOT include instructions, bullet points, symbols, or formatting."
    )

    if not rewrite_only:
        instruction += f" Translate it into {target_language}."

    prompt = f"""
{instruction}

Rules:
- No asterisks (*), bullets, hyphens, or markdown
- Expand numbers naturally (158 → one hundred fifty eight)
- Phone numbers should be spoken in groups (98765 43210 → nine eight seven six five, four three two one zero)
- Natural, flowing narration
- No headings or meta text

Text:
{text}
"""

    return _call_llm(prompt)
