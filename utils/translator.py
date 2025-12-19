from deep_translator import GoogleTranslator     # Import GoogleTranslator for translation functionality

def translate_text(text, target_lang="hi"):      # Translate text to the specified target language.
    if not text:
        return ""

    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # fallback: return original

