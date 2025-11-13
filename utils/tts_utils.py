"""
Helpers for TTS:
- gTTS: simpler online MP3 output
- pyttsx3: offline, writes WAV
"""

def tts_gtts_save(text: str, out_path: str, lang: str = "en"):
    try:
        from gtts import gTTS
    except Exception as e:
        raise RuntimeError("gTTS not installed. pip install gTTS") from e
    t = gTTS(text=text, lang=lang)
    t.save(out_path)

def tts_pyttsx3_save(text: str, out_path: str):
    try:
        import pyttsx3
    except Exception as e:
        raise RuntimeError("pyttsx3 not installed. pip install pyttsx3") from e

    engine = pyttsx3.init()
    # try to set some properties (rate/volume) - optional
    try:
        engine.setProperty('rate', 150)
    except Exception:
        pass
    engine.save_to_file(text, out_path)
    engine.runAndWait()
    engine.stop()
