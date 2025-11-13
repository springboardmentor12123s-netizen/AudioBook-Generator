# modules/tts_engine.py
import os
import pyttsx3
from pathlib import Path
import wave

def tts_save_pyttsx3(text: str, out_path: str):
    engine = pyttsx3.init()
    rate = engine.getProperty("rate")
    engine.setProperty("rate", int(rate * 0.95))
    engine.save_to_file(text, out_path)
    engine.runAndWait()
    engine.stop()

def combine_wav_files(wav_paths, out_path):
    if not wav_paths:
        raise ValueError("No wav files to combine.")
    data = []
    params = None
    for p in wav_paths:
        with wave.open(p, 'rb') as w:
            if params is None:
                params = w.getparams()
            else:
                pparams = w.getparams()
                if (pparams.nchannels, pparams.sampwidth, pparams.framerate) != (params.nchannels, params.sampwidth, params.framerate):
                    raise RuntimeError("WAV parameter mismatch.")
            data.append(w.readframes(w.getnframes()))
    with wave.open(out_path, 'wb') as out:
        out.setnchannels(params.nchannels)
        out.setsampwidth(params.sampwidth)
        out.setframerate(params.framerate)
        for frames in data:
            out.writeframes(frames)
