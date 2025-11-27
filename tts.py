# tts.py
import os
import tempfile
from pydub import AudioSegment
import pyttsx3

def text_to_wav(text, out_wav_path, rate=None):
    """
    Uses pyttsx3 to create a WAV file saved to out_wav_path
    """
    engine = pyttsx3.init()
    if rate is not None:
        engine.setProperty('rate', rate)
    # Optionally change voice (commented):
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)

    # pyttsx3 can save directly:
    engine.save_to_file(text, out_wav_path)
    engine.runAndWait()
    return out_wav_path

def wav_to_mp3(wav_path, mp3_path):
    """
    Convert WAV to MP3 using pydub (requires ffmpeg on system)
    """
    audio = AudioSegment.from_file(wav_path, format="wav")
    audio.export(mp3_path, format="mp3")
    return mp3_path

def text_to_audio(text, out_path_base, prefer_mp3=True, rate=150):
    """
    text -> wav (pyttsx3) -> optionally mp3
    out_path_base: path without extension, e.g., './output/mybook'
    returns filepath of final audio
    """
    wav_path = f"{out_path_base}.wav"
    mp3_path = f"{out_path_base}.mp3"

    text_to_wav(text, wav_path, rate=rate)

    if prefer_mp3:
        try:
            wav_to_mp3(wav_path, mp3_path)
            return mp3_path
        except Exception as e:
            print("Could not convert to mp3 (ffmpeg missing?), returning wav. Error:", e)
            return wav_path
    else:
        return wav_path