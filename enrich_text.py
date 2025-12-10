import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def enrich_text(text):
    prompt = (
        "Rewrite the following text in an engaging, listener-friendly audiobook narration style.\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    return response.text



