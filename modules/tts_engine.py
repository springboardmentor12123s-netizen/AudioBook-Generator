# modules/tts_engine.py
import os
import asyncio
import edge_tts
import datetime
import hashlib

AUDIO_DIR = "generated_audio"

# Create directory if not exists
os.makedirs(AUDIO_DIR, exist_ok=True)


def _generate_unique_filename(text: str) -> str:
    """Generate a unique filename using timestamp + text hash."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    short_hash = hashlib.md5(text.encode()).hexdigest()[:6]
    filename = f"audiobook_{timestamp}_{short_hash}.mp3"
    return os.path.join(AUDIO_DIR, filename)


async def _edge_tts_generate(text, file_path):
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.save(file_path)


def generate_audio(text: str):
    """
    Generate MP3 audio using EDGE-TTS and SAVE it in generated_audio/ folder.
    Returns (file_path, mime_type).
    """
    try:
        file_path = _generate_unique_filename(text)
        asyncio.run(_edge_tts_generate(text, file_path))
        return file_path, "audio/mp3"
    except Exception as e:
        print("EDGE-TTS Error:", e)
        return None, None
