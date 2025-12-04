# utils/gemini_rewriter.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-1.5-pro"   # you can change to gemini-2.0 when available


def rewrite_audiobook_style(text: str) -> str:
    """
    Rewrite text in audiobook narration style using Google Gemini.
    Keeps meaning same but improves storytelling flow.
    """
    prompt = (
        "Rewrite the following text in a professional audiobook narration style. "
        "Keep it engaging, emotional, clear and immersive. Do NOT add new facts.\n\n"
        f"TEXT:\n{text}"
    )

    response = genai.GenerativeModel(MODEL).generate_content(prompt)
    return response.text.strip()
