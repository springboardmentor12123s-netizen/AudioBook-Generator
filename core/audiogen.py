# core/audiogen.py
from gtts import gTTS
from pathlib import Path
from datetime import datetime

def text_to_speech(text: str, filename: str = None, language: str = "en") -> str:
    """
    Convert text to speech using gTTS and save as an MP3 in core/output/.
    Returns: absolute path to saved mp3 file as string.
    Raises RuntimeError on failure.
    """
    try:
        if not text or not str(text).strip():
            raise ValueError("Input text is empty. Nothing to convert to speech.")

        # Save inside the core folder, so you can see it in your project explorer
        base_dir = Path(__file__).parent.resolve()   # <project>/core
        output_dir = base_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Unique filename by default to avoid overwrite
        if filename:
            # ensure extension
            filename = str(filename)
            if not filename.lower().endswith(".mp3"):
                filename = filename + ".mp3"
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audiobook_{ts}.mp3"

        output_path = output_dir / filename

        # Generate MP3 via gTTS (requires internet)
        tts = gTTS(text=text, lang=language)
        tts.save(str(output_path))

        # Return absolute string path
        return str(output_path.resolve())

    except Exception as e:
        # Raise a RuntimeError so callers can handle it cleanly
        raise RuntimeError(f"TTS generation failed: {e}")
