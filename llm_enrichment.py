
import os
import google.generativeai as genai

def enrich_text_for_audio(text, model_name="gemini-1.5-flash", temperature=0.8):
    """
    Enhances raw extracted text into an audiobook-style narration using Google's Gemini API.
    """
    
    # Ensure configuration is loaded at runtime
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment."
    genai.configure(api_key=api_key)

    # Validate model availability
    try:
        available_models = [m.name for m in genai.list_models()]
        # Check if the requested model (e.g., 'models/gemini-1.5-flash') is available
        # The list_models() returns names like 'models/gemini-pro'
        target_model = f"models/{model_name}" if not model_name.startswith("models/") else model_name
        
        if target_model not in available_models:
             print(f"⚠️ Requested model {target_model} not found. Available models: {available_models}")
             # Fallback to gemini-pro or the first available generateContent model
             for m in genai.list_models():
                 if 'generateContent' in m.supported_generation_methods:
                     model_name = m.name # use the full name e.g. 'models/gemini-pro'
                     print(f"👉 Switching to fallback model: {model_name}")
                     break
    except Exception as e:
        print(f"⚠️ Could not list models: {e}")
        # Proceed with default and hope for the best


    if not text or len(text.strip()) < 10:
        return "Error: No valid text provided for enrichment."

    # Chunk text (Gemini also has token limits)
    MAX_CHARS = 5000
    text_chunks = [text[i:i + MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]
    enriched_output = ""

    for chunk in text_chunks:
        prompt = f"""
        Rewrite the following text so it sounds engaging, emotional, and suitable for audiobook narration.
        Make it flow like a professional storyteller's script but keep the original meaning intact.

        Text:
        {chunk}
        """

        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=1024
                )
            )

            if response:
                # Use .text property which handles candidate checks internally
                # (raises ValueError if blocked by safety settings)
                try:
                    enriched_output += response.text + "\n"
                except ValueError:
                    # If response was blocked
                    print("⚠️ Gemini response blocked or empty.")
                    enriched_output += chunk
            else:
                enriched_output += chunk

        except Exception as e:
            print("⚠️ Gemini Error:", e)
            enriched_output += chunk

    return enriched_output.strip()
