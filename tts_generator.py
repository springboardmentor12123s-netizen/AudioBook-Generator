# tts_generator.py

from config import TTS_ENGINE, TTS_OUTPUT_FORMAT
from TTS.api import TTS
import pyttsx3

def text_to_speech_coqui(text, output_file="audiobook.wav"):
    try:
        tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)
        tts.tts_to_file(text=text, file_path=output_file)
        return output_file
    except Exception as e:
        print("Coqui error → using fallback:", e)
        return text_to_speech_pyttsx3(text, output_file)

def text_to_speech_pyttsx3(text, output_file="audiobook_fallback.mp3"):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1.0)
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file

def generate_audiobook(text, output_path="audiobook_output.wav"):

    if TTS_ENGINE.lower() == "coqui":
        return text_to_speech_coqui(text, output_path)

    elif TTS_ENGINE.lower() == "pyttsx3":
        return text_to_speech_pyttsx3(text, output_path)

    else:
        print("Invalid TTS engine in .env — defaulting to pyttsx3")
        return text_to_speech_pyttsx3(text, output_path)
