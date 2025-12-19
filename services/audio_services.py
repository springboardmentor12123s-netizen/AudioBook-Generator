"""
audio_service.py
------------------------------------------------------
This service layer connects the main app with:
- Text-to-Speech engine (generate audiobook)
- Audio transcription (lyrics extraction)
- General audio-related operations

We keep this layer so:
- app.py stays clean
- Code is easier to maintain
- Mentor can clearly see modular architecture
------------------------------------------------------
"""

from gtts import gTTS
import os
import time

def generate_speech(text, voice_type="female"):
    if voice_type.lower() == "female":
        lang = "en"
        tld = "co.uk"
    elif voice_type.lower() == "male":
        lang = "en"
        tld = "co.in"
    else:
        lang = "en"
        tld = "com"

    tts = gTTS(text=text, lang=lang, tld=tld)

    os.makedirs("outputs", exist_ok=True)
    file_path = f"outputs/audiobook_{int(time.time())}.mp3"
    tts.save(file_path)

    return file_path
