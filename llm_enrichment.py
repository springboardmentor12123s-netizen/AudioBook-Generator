# llm_enrichment.py

import os
import google.generativeai as genai

# Configure the Gemini API key (set as an environment variable)
# Example:
#   export GEMINI_API_KEY="your_api_key_here"
# or in Windows PowerShell:
#   setx GEMINI_API_KEY "your_api_key_here"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def enrich_text_for_audio(text, model_name="gemini-1.5-flash", temperature=0.8):
    """
    Enhances raw extracted text into an audiobook-style narration using Google's Gemini API.
    - Adds natural tone, rhythm, and emotion.
    - Keeps meaning and clarity intact.
    """

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

            if response and response.candidates:
                enriched_output += response.candidates[0].content.parts[0].text + "\n"
            else:
                enriched_output += chunk  # fallback if no response

        except Exception as e:
            print("⚠️ Error during Gemini processing:", e)
            enriched_output += chunk

    return enriched_output.strip()
