# list_gemini_models.py
import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("❌ GEMINI_API_KEY not set in environment")

genai.configure(api_key=api_key)

print("Fetching available Gemini models...\n")

models = list(genai.list_models())   # convert generator → list

for m in models:
    # extract name safely across SDK versions
    try:
        model_name = getattr(m, "name", None) or m.get("name")
    except Exception:
        model_name = str(m)

    # extract display name if present
    try:
        display = getattr(m, "display_name", None) or m.get("displayName", "")
    except Exception:
        display = ""

    print(f"- {model_name}  |  {display}")
