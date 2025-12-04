# utils/tts.py

import os
from pathlib import Path
from typing import Tuple

from gtts import gTTS


def text_to_speech_mp3(
    text: str,
    output_dir: str = "outputs/audio",
    base_name: str = "audiobook",
    lang: str = "en",
    slow: bool = False,
    tld: str = "com",  # 'com', 'co.in', 'co.uk', 'com.au' etc.
) -> Tuple[str, bytes]:
    """
    Convert text to MP3 using gTTS.
    Returns (file_path, file_bytes).
    """
    if not text.strip():
        raise ValueError("Empty text – nothing to convert to audio.")

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Make a safe file name
    safe_name = "".join(c for c in base_name if c.isalnum() or c in ("_", "-")).rstrip()
    file_path = os.path.join(output_dir, f"{safe_name}.mp3")

    # gTTS call
    tts = gTTS(text=text, lang=lang, slow=slow, tld=tld)
    tts.save(file_path)

    with open(file_path, "rb") as f:
        data = f.read()

    return file_path, data
