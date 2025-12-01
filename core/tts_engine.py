import os
from gtts import gTTS


def text_to_speech(
    text: str,
    output_path: str,
    lang: str = "en",
    slow: bool = False,
) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    safe_text = text[:4500]  # basic safety limit for gTTS [web:70]
    tts = gTTS(text=safe_text, lang=lang, slow=slow)
    tts.save(output_path)
    return output_path
