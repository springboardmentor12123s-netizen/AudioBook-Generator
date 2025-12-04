# utils/enrich_text.py

import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"



def enrich_for_audiobook(text: str) -> str:
    if not text.strip():
        return ""

    prompt = (
        "Rewrite the following text for an engaging audiobook narration. "
        "Keep the meaning accurate, but improve flow, clarity and emotional impact. "
        "Do NOT add new facts.\n\n"
        f"TEXT:\n{text}"
    )

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return (response.text or "").strip()
