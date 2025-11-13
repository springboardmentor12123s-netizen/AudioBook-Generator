# list_models.py
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=api_key)

# List available models
print("\n✅ Available Gemini Models:")
for model in genai.list_models():
    print("-", model.name)
