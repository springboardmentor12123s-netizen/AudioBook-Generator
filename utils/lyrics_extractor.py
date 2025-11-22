"""
lyrics_extractor.py
---------------------------------------------
This file extracts lyrics from an uploaded audio file
using the Whisper ASR (Automatic Speech Recognition) model.

Whisper Base model features:
- Good speed
- Decent accuracy
- Works well for English + Hindi + mixed language songs
- Lightweight and works on CPU also

Steps performed:
1. Load the Whisper model (base)
2. Transcribe the audio
3. Return text (lyrics)
4. Clean the text slightly for readability
---------------------------------------------
"""

import whisper


# ------------------------------------------------------
# Load Whisper base model only once (saves processing time)
# ------------------------------------------------------
model = whisper.load_model("base")


def extract_lyrics_from_audio(audio_path):
    """
    Extracts lyrics (transcription) from an audio file.

    Parameters:
        audio_path (str): Path where the audio file is saved.

    Returns:
        lyrics (str): Extracted text / lyrics.
    """

    # -----------------------------------------------
    # Step 1: Transcribe using Whisper Base model
    # -----------------------------------------------
    result = model.transcribe(audio_path)

    # Whisper returns a dictionary with many fields:
    # result["text"] → contains the full transcription
    
    lyrics = result.get("text", "").strip()

    # -----------------------------------------------
    # Step 2: If empty transcription
    # -----------------------------------------------
    if lyrics == "":
        return "❌ No lyrics detected. The audio may be unclear."

    # -----------------------------------------------
    # Step 3: Fix basic punctuation spacing
    # -----------------------------------------------
    lyrics = (
        lyrics.replace(" ,", ",")
              .replace(" .", ".")
              .replace(" ?", "?")
              .replace(" !", "!")
    )

    # -----------------------------------------------
    # Step 4: Return cleaned lyrics
    # -----------------------------------------------
    return lyrics
