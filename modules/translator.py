# modules/translator.py
from googletrans import Translator

_trans = Translator()

LANG_CODE_MAP = {
    "en": "en",
    "hi": "hi",
    "fr": "fr",
    "es": "es",
    "ta": "ta",
    "te": "te",
}

def translate_text(text: str, dest_lang: str) -> str:
    """
    Translate `text` to dest_lang (language code like 'hi','fr','es','ta','te').
    If dest_lang is 'en' or translator fails, returns original text.
    """
    if not text or not dest_lang:
        return text

    dest = LANG_CODE_MAP.get(dest_lang, dest_lang)
    if dest == "en":
        return text  # no translation needed

    try:
        result = _trans.translate(text, dest=dest)
        return result.text
    except Exception as e:
        # fallback: return original if translation fails
        print("Translation error:", e)
        return text
