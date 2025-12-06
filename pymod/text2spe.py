# pymod/text2spe.py
"""
Single-file TTS utility used by the Streamlit app.
Exposes: synthesize_text_to_single_file(text, out_dir, out_name="audiobook_final", method="gtts", lang="en")
Returns path to created audio file (wav or mp3).
"""

import os
from pathlib import Path
from typing import Optional

def _ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def synthesize_text_to_single_file(text: str, out_dir: str, out_name: str = "audiobook_final", method: str = "gtts", lang: str = "en") -> str:
    """
    Synthesizes entire text to a single audio file.
    method: "gtts" (fast, needs internet) or "pyttsx3" (offline).
    Returns path to final WAV (or MP3 if pydub not available).
    """
    _ensure_dir(out_dir)
    out_base = Path(out_dir) / out_name
    mp3_path = out_base.with_suffix(".mp3")
    wav_path = out_base.with_suffix(".wav")

    text = (text or "").strip()
    if not text:
        # create a 1-second silent wav to avoid errors
        import wave, struct
        with wave.open(str(wav_path), "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(22050)
            wf.writeframes(b"\x00\x00" * 22050)  # 1 second silence
        return str(wav_path)

    if method == "gtts":
        # fast, but requires internet
        try:
            from gtts import gTTS
        except Exception as e:
            raise RuntimeError(f"gTTS not installed or failed import: {e}")

        max_chunk = 3500  # safe chunk size for gTTS
        if len(text) <= max_chunk:
            tts = gTTS(text=text, lang=lang)
            tts.save(str(mp3_path))
        else:
            # split by sentence-ish boundaries
            import re
            parts = []
            cur = ""
            for seg in re.split(r'(?<=[\.\?\!])\s+', text):
                if len(cur) + len(seg) < max_chunk:
                    cur = (cur + " " + seg).strip()
                else:
                    if cur:
                        parts.append(cur)
                    cur = seg
            if cur:
                parts.append(cur)

            # try to combine parts using pydub if available
            try:
                from pydub import AudioSegment
                tmp_files = []
                for i, p in enumerate(parts):
                    tmp = out_base.with_name(f"{out_base.name}_part{i}.mp3")
                    gTTS(text=p, lang=lang).save(str(tmp))
                    tmp_files.append(tmp)
                combined = AudioSegment.empty()
                for t in tmp_files:
                    combined += AudioSegment.from_file(t)
                    t.unlink(missing_ok=True)
                combined.export(str(mp3_path), format="mp3")
            except Exception:
                # fallback: save parts separately and raise to indicate pydub missing
                for i, p in enumerate(parts):
                    gTTS(text=p, lang=lang).save(str(out_base.with_name(f"{out_base.name}_part{i}.mp3")))
                raise RuntimeError("Text too long; pydub required to concatenate parts. Install pydub and ffmpeg or shorten text.")

        # convert mp3->wav if pydub available
        try:
            from pydub import AudioSegment
            seg = AudioSegment.from_file(mp3_path)
            seg.export(str(wav_path), format="wav")
            mp3_path.unlink(missing_ok=True)
            return str(wav_path)
        except Exception:
            # return mp3 path if conversion not possible (Streamlit can play mp3)
            return str(mp3_path)

    elif method == "pyttsx3":
        try:
            import pyttsx3
        except Exception as e:
            raise RuntimeError(f"pyttsx3 not installed or failed import: {e}")
        engine = pyttsx3.init()
        try:
            rate = engine.getProperty("rate")
            engine.setProperty("rate", int(rate * 0.95))
        except Exception:
            pass
        # save single file
        engine.save_to_file(text, str(wav_path))
        engine.runAndWait()
        return str(wav_path)
    else:
        raise ValueError("Unknown method; choose 'gtts' or 'pyttsx3'.")
