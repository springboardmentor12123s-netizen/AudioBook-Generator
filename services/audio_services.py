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

from utils.tts_engine import generate_speech
from utils.lyrics_extractor import extract_lyrics_from_audio


# ------------------------------------------------------
# Generate audiobook from text
# ------------------------------------------------------
def create_audiobook(text, voice_type):
    """
    Wrapper for generate_speech() from tts_engine.py

    Parameters:
        text (str): Input text.
        voice_type (str): Selected voice type.

    Returns:
        audio_path (str): Path to generated MP3 file.
    """
    return generate_speech(text, voice_type)


# ------------------------------------------------------
# Extract lyrics from uploaded audio
# ------------------------------------------------------
def get_lyrics(audio_path):
    """
    Wrapper for extract_lyrics_from_audio().

    Parameters:
        audio_path (str): Path to the uploaded audio file.

    Returns:
        lyrics (str): Extracted song lyrics.
    """
    return extract_lyrics_from_audio(audio_path)
