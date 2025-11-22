"""
tts_engine.py
---------------------------------------
Handles converting text into spoken audio (MP3 format).

We use gTTS because:
- It supports multiple accents
- Very lightweight
- Easy to use for projects
- Fast and free

Voice selection is simulated by changing the language accent.
gTTS does not support true male/female voice, but accents differ slightly.
---------------------------------------
"""

from gtts import gTTS
import os
import time


def generate_speech(text, voice_type="Default"):
    """
    Converts text into speech and saves it as an MP3 file.

    Parameters:
        text (str): Text that needs to be converted to audio.
        voice_type (str): Selected voice type (Default, Female, Male).

    Returns:
        file_path (str): Path of the generated MP3 file.
    """

    # -----------------------------------------
    # Voice Selection (Simulated Accent Change)
    # -----------------------------------------
    # Default: normal English
    # Female: softer English accent
    # Male: Indian accent (example)
    # Note: gTTS does not support real male/female voices,
    #       but we simulate by choosing different accents.
    # -----------------------------------------

    if voice_type == "Female":
        lang = "en"        # English Female
        tld = "co.uk"      # UK accent
    elif voice_type == "Male":
        lang = "en"        # English Male
        tld = "co.in"      # Indian accent (stronger tone)
    else:
        lang = "en"
        tld = "com"        # Default English

    # -----------------------------------------
    # Generate speech
    # -----------------------------------------
    tts = gTTS(text=text, lang=lang, tld=tld)

    # Create output filename with timestamp
    timestamp = int(time.time())
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    file_path = os.path.join(output_folder, f"audiobook_{timestamp}.mp3")

    # Save MP3 file
    tts.save(file_path)

    return file_path
