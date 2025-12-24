import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=API_KEY)

print("\nListing available models:\n")

try:
    for model in genai.list_models():
        methods = ", ".join(model.supported_generation_methods)
        print(f"- {model.name} | methods: {methods}")
except Exception as e:
    print("Failed to list models:")
    print(e)
