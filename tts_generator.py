# tts_generator.py

import os
from TTS.api import TTS
import pyttsx3

def text_to_speech_coqui(text, output_file="audiobook.wav"):
    """
    Converts enriched text into high-quality audiobook audio using Coqui TTS.
    Works best with Python 3.10–3.11 and supports multiple voices.
    """
    try:
        # Load a pretrained TTS model (English VITS voice)
        tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)
        tts.tts_to_file(text=text, file_path=output_file)
        print(f"✅ Coqui TTS: Audio file saved as {output_file}")
        return output_file

    except Exception as e:
        print(f"⚠️ Coqui TTS failed: {e}")
        print("👉 Switching to pyttsx3 fallback.")
        return text_to_speech_pyttsx3(text, output_file)


def text_to_speech_pyttsx3(text, output_file="audiobook_fallback.mp3"):
    """
    Fallback offline TTS using pyttsx3.
    Produces a simpler robotic voice, but fully offline and reliable.
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)    # narration speed
        engine.setProperty("volume", 1.0)  # max volume
        voices = engine.getProperty("voices")
        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)  # use female/male alt voice
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        print(f"✅ pyttsx3: Audio file saved as {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ pyttsx3 failed: {e}")
        return None


def generate_audiobook(text, output_path="audiobook_output.wav"):
    """
    Wrapper to handle audio generation from enriched text.
    """
    if not text or len(text.strip()) < 10:
        print("⚠️ No valid text to convert.")
        return None
    return text_to_speech_coqui(text, output_file=output_path)
