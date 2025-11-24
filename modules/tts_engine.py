# modules/tts_engine.py
import os
import asyncio
import edge_tts
import datetime
import hashlib

AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Basic language -> default voices mapping (you can extend this)
LANG_VOICES = {
    "en": [
        ("en-US-JennyNeural", "English - Jenny (female)"),
        ("en-US-GuyNeural", "English - Guy (male)")
    ],
    "hi": [
        ("hi-IN-MadhurNeural", "Hindi - Madhur"),
        ("hi-IN-PrabhatNeural", "Hindi - Prabhat")
    ],
    "es": [
        ("es-ES-AlvaroNeural", "Spanish (Spain) - Alvaro"),
        ("es-ES-ElviraNeural", "Spanish (Spain) - Elvira")
    ],
    "fr": [
        ("fr-FR-DeniseNeural", "French - Denise"),
        ("fr-FR-HenriNeural", "French - Henri")
    ],
    "ta": [
        ("ta-IN-PallaviNeural", "Tamil - Pallavi")
    ],
    "te": [
        ("te-IN-GayatriNeural", "Telugu - Gayatri")
    ],
    # add more languages/voices as needed
}


def _generate_filename(text: str, ext: str = ".mp3") -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    short = hashlib.md5(text.encode("utf-8")).hexdigest()[:8]
    return os.path.join(AUDIO_DIR, f"audiobook_{ts}_{short}{ext}")


async def _edge_tts_save(text: str, voice: str, out_path: str):
    # Communciate supports long text; it will chunk internally
    communicator = edge_tts.Communicate(text, voice=voice)
    await communicator.save(out_path)


def generate_audio(text: str, lang: str = "en", voice: str | None = None):
    """
    Generate MP3 using edge-tts for a given language+voice.
    - text: input text
    - lang: language code (e.g. 'en','hi','es')
    - voice: full voice id string (overrides default)
    Returns: (file_path, "audio/mp3") or (None, None) on failure
    """
    if not text or not text.strip():
        return None, None

    # pick voice
    if voice is None:
        if lang in LANG_VOICES and len(LANG_VOICES[lang]) > 0:
            voice = LANG_VOICES[lang][0][0]
        else:
            voice = "en-US-JennyNeural"

    out_path = _generate_filename(text, ext=".mp3")
    try:
        asyncio.run(_edge_tts_save(text, voice, out_path))
        if os.path.exists(out_path):
            return out_path, "audio/mp3"
    except Exception as e:
        # fallback: print error and return None
        print("edge-tts error:", e)
        return None, None

    return None, None
