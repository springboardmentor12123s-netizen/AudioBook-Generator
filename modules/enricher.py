"""
LLM Enrichment Module
Enhances text for audiobook narration using Gemini API
"""

import google.generativeai as genai


PROMPT_TEMPLATE = """Rewrite this text for audiobook narration. Make it natural, conversational, and easy to listen to.

STRICT RULES:
- Output ONLY the rewritten text in {language}
- Do NOT include any introduction like "Here is" or "Sure" or "Okay"
- Do NOT include any headers or labels
- Do NOT explain what you did
- Start directly with the rewritten content
- The output MUST be in {language} language

Text to rewrite:
{text}"""


LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "pl": "Polish",
    "hi": "Hindi",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian",
    "nl": "Dutch",
    "tr": "Turkish",
    "sv": "Swedish",
    "id": "Indonesian",
    "fil": "Filipino",
    "ta": "Tamil",
    "uk": "Ukrainian",
    "el": "Greek",
    "cs": "Czech",
    "fi": "Finnish",
    "ro": "Romanian",
    "da": "Danish",
    "bg": "Bulgarian",
    "ms": "Malay",
    "sk": "Slovak",
    "hr": "Croatian",
}


def get_available_languages():
    """Get list of available languages"""
    return LANGUAGES


def enrich_text(raw_text, api_key, language="English"):
    """
    Enhance text for audiobook narration using Gemini API

    Args:
        raw_text: The extracted text to enhance
        api_key: Gemini API key
        language: Target language for output

    Returns:
        dict: {"success": True, "text": "..."} or {"success": False, "error": "..."}
    """
    try:
        if not api_key:
            return {"success": False, "error": "Gemini API key not configured"}

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-flash-lite-latest")

        # Truncate text if too long (Gemini has token limits)
        max_chars = 30000
        if len(raw_text) > max_chars:
            raw_text = raw_text[:max_chars] + "..."

        # Generate enhanced text
        prompt = PROMPT_TEMPLATE.format(text=raw_text, language=language)
        response = model.generate_content(prompt)

        enhanced_text = response.text.strip()

        if not enhanced_text:
            return {"success": False, "error": "LLM returned empty response"}

        return {"success": True, "text": enhanced_text}

    except Exception as e:
        return {"success": False, "error": str(e)}


def enrich_text_simple(raw_text):
    """
    Simple fallback - just clean up text without LLM
    Used when API key is not available

    Args:
        raw_text: The extracted text

    Returns:
        dict: {"success": True, "text": "..."}
    """
    # Basic cleanup
    text = raw_text.replace("\n\n\n", "\n\n")
    text = text.replace("  ", " ")
    return {"success": True, "text": text}
