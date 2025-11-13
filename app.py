# app.py
"""
AudioBook Generator - Streamlit app
Features:
- Fast extraction (PDF via PyMuPDF, DOCX, TXT)
- LLM rewrite options: Gemini (cloud) or Local quick rewrite (fallback)
- Quota-safe Gemini usage with retries and retry_delay honoring
- TTS: gTTS (online) with pyttsx3+pydub offline fallback
- Plays audio in UI and offers download
- Uses .env for GEMINI_API_KEY and optional FFMPEG_PATH
"""

import os
import time
from io import BytesIO
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

# load environment variables from .env if present
load_dotenv()

# fast PDF extraction
import fitz  # PyMuPDF

# docx
from docx import Document

# modules (assumed to exist in modules/ folder)
from modules.llm_enrichment import (
    enrich_text_with_gemini_quota_safe,
    simple_local_enrich,
)
from modules.tts_engine import generate_audio  # returns path to mp3 or None

# Config
st.set_page_config(page_title="AudioBook Generator", page_icon="🎧", layout="wide")
st.title("🎧 AudioBook Generator")
st.markdown(
    "Upload PDF / DOCX / TXT → choose rewrite mode (optional) → Generate & play audiobook MP3."
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip() or None
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "").strip() or None

if FFMPEG_PATH:
    # modules.tts_engine already handles pydub config, but this ensures pydub sees it early
    try:
        from pydub import AudioSegment
        AudioSegment.converter = FFMPEG_PATH
    except Exception:
        pass


# -------------------------
# Utility: fast extraction
# -------------------------
def extract_text_from_file(uploaded_file, preview_only: bool = False) -> str:
    """
    Extract text from PDF (fast via PyMuPDF), DOCX, or TXT.
    If preview_only=True, only extract first 1-2 pages for PDF to be quick.
    """
    name = uploaded_file.name.lower()
    data = uploaded_file.read()
    uploaded_file.seek(0)

    try:
        if name.endswith(".pdf"):
            doc = fitz.open(stream=data, filetype="pdf")
            num_pages = doc.page_count
            pages_to_read = min(num_pages, 2) if preview_only else num_pages
            texts = []
            for i in range(pages_to_read):
                page = doc.load_page(i)
                texts.append(page.get_text("text") or "")
            doc.close()
            return "\n\n".join(texts).strip()

        if name.endswith(".docx"):
            docx = Document(BytesIO(data))
            paras = [p.text for p in docx.paragraphs if p.text]
            return "\n\n".join(paras).strip()

        if name.endswith(".txt"):
            return data.decode("utf-8", errors="ignore").strip()

    except Exception as e:
        st.error(f"Extraction error: {e}")
        return ""

    st.error("Unsupported file type.")
    return ""


# -------------------------
# Main UI
# -------------------------
uploaded = st.file_uploader("Upload a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
if not uploaded:
    st.info("Upload a file to begin. For quick tests, upload a small .txt file.")
    st.stop()

# Extract preview first (fast)
with st.spinner("Extracting preview..."):
    preview_text = extract_text_from_file(uploaded, preview_only=True)

if not preview_text:
    st.error("Could not extract text from the uploaded file. Try a different file.")
    st.stop()

st.success("Preview extracted.")
if st.checkbox("Show extracted preview"):
    st.text_area("Preview (first pages)", preview_text, height=250)

# Option: extract full text on demand (button)
full_text = None
if st.button("Extract full text"):
    with st.spinner("Extracting full text (may take a while for large PDFs)..."):
        full_text = extract_text_from_file(uploaded, preview_only=False)
    if not full_text:
        st.error("Full extraction failed or produced no text.")
        st.stop()
    st.success("Full text extracted.")
    if st.checkbox("Show full extracted text"):
        st.text_area("Full extracted text", full_text[:20000], height=400)

# If full_text not yet extracted, use preview_text as the working text for quick operations
working_text = full_text if full_text else preview_text

# -------------------------
# Rewrite mode selection
# -------------------------
st.markdown("### Rewrite options (optional)")
mode = st.radio(
    "Choose rewrite mode",
    options=["No rewrite", "Local quick rewrite (fast, offline)", "Gemini (cloud, may use quota)"],
    index=1,
)

rewritten_text = working_text  # default

if mode == "Local quick rewrite (fast, offline)":
    if st.button("Apply local quick rewrite"):
        with st.spinner("Applying local quick rewrite..."):
            rewritten_text = simple_local_enrich(working_text)
        st.success("Local rewrite complete.")
        st.text_area("Rewritten (local) preview", rewritten_text[:20000], height=300)

elif mode == "Gemini (cloud, may use quota)":
    st.info("Gemini calls consume API quota. Use 'Quick preview' to conserve quota.")
    # quick preview toggle
    preview_only = st.checkbox("Quick preview (rewrite first 3000 chars)", value=True)
    model_choice = st.selectbox(
        "Gemini model",
        options=[
            "models/gemini-2.5-flash",
            "models/gemini-2.5-pro",
            "models/gemini-flash-latest",
        ],
        index=0,
    )
    max_req_min = st.slider("Max Gemini requests per minute (throttle)", 1, 60, 10)
    if st.button("Rewrite with Gemini"):
        text_for_rewrite = working_text[:3000] if preview_only else working_text
        with st.spinner("Rewriting with Gemini (quota-safe)..."):
            rewritten_text = enrich_text_with_gemini_quota_safe(
                text_for_rewrite,
                model=model_choice,
                max_retries_per_chunk=3,
                throttle_seconds_between_calls=1.2,
                max_requests_per_minute=max_req_min,
                use_local_on_failure=True,
            )
        st.success("Gemini rewrite finished (or local fallback used).")
        st.text_area("Rewritten (Gemini) preview", rewritten_text[:20000], height=300)

else:
    # No rewrite selected
    rewritten_text = working_text

# -------------------------
# Allow user to edit before TTS
# -------------------------
st.markdown("### Edit text before generating audio (optional)")
edited_text = st.text_area("Text to convert to audio", rewritten_text[:200000], height=300)

# -------------------------
# Generate audio
# -------------------------
st.markdown("### Generate audio")
if st.button("🎧 Generate Audio"):
    if not edited_text.strip():
        st.error("No text to convert.")
    else:
        with st.spinner("Generating audio..."):
            audio_path, mime = generate_audio(edited_text)

        if audio_path:
            st.success("Audio generated & saved!")

            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format=mime)

            st.download_button(
                "⬇ Download MP3",
                data=audio_bytes,
                file_name=os.path.basename(audio_path),
                mime=mime
            )

            st.info(f"Saved file: `{audio_path}`")

        else:
            st.error("Audio generation failed.")



# Footer
st.markdown("---")
st.caption("Notes: Gemini requires GEMINI_API_KEY set in environment (.env). Local rewrite is fast and does not use quota.")
