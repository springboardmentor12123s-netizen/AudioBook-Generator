import re
from gtts import gTTS
from pathlib import Path

LANGUAGE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Marathi": "mr",
    "Odia": "or"
}

def _clean_text_for_audio(text: str) -> str:
    # Remove bullets, symbols
    text = re.sub(r"[*_•\-]+", " ", text)

    # Normalize phone numbers (grouped reading)
    text = re.sub(
        r"(\d{5})\s*(\d{5})",
        r"\1 \2",
        text
    )

    # Remove excessive spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def synthesize_text_to_single_file(
    text: str,
    out_dir: str,
    out_name: str,
    lang: str,
):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    cleaned_text = _clean_text_for_audio(text)

    # Slightly faster speech
    tts = gTTS(
        text=cleaned_text,
        lang=lang,
        slow=False
    )

    output_file = out_path / f"{out_name}.mp3"
    tts.save(str(output_file))

    return str(output_file)
