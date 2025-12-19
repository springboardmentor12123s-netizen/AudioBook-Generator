"""
lyrics_extractor.py
---------------------------------------------
This file extracts lyrics from an uploaded audio file
using the Whisper ASR (Automatic Speech Recognition) model.

Whisper Base model features:
- Good speed
- Decent accuracy
- Works well for English + Hindi + mixed language songs
- Lightweight and works on CPU also.

Steps performed:
1. Load the Whisper model (base)
2. Transcribe the audio
3. Return text (lyrics)
4. Clean the text slightly for readability
---------------------------------------------
"""
import json
from vosk import Model, KaldiRecognizer
import wave
import subprocess
import os

def extract_lyrics_from_audio(audio_path, model_path="models/vosk-model-small-en-us-0.15"):
    wav_file = "temp_audio.wav"     # Temporary WAV file for processing

    subprocess.call([               
        "ffmpeg", "-y",
        "-i", audio_path,
        "-ar", "16000",
        "-ac", "1",
        wav_file
    ])

    if not os.path.exists(model_path):                                   # Check if the model exists
        raise FileNotFoundError("Vosk model missing at: " + model_path)  #Error if model not found

    model = Model(model_path)                           # Load the Vosk model
    wf = wave.open(wav_file, "rb")                      # Open the WAV file
    rec = KaldiRecognizer(model, wf.getframerate())     # Initialize recognizer with model and sample rate

    output = ""
    while True:
        data = wf.readframes(4000)                               # Read audio frames
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):                             # Process the audio chunk
            output += json.loads(rec.Result())["text"] + " "     # Append recognized text

    output += json.loads(rec.FinalResult())["text"]              # Finalize and get remaining text
    return output.strip()
