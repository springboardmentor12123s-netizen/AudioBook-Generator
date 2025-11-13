# app_streamlit_final.py
import os, tempfile
import streamlit as st
from pathlib import Path
from pymod.text_extraction import extract_text
from pymod.llm import enrich_text
from pymod.utils import chunk_text_by_chars, safe_write_text, clean_extracted_text
from pymod.text2spe import tts_save_pyttsx3, combine_wav_files

st.set_page_config(page_title="AI AudioBook Generator", layout="centered")
st.title("🎧 AI AudioBook Generator — Gemini (mandatory)")

# enforce that GEMINI_API_KEY is present before processing
if not os.environ.get("GEMINI_API_KEY"):
    st.error("GEMINI_API_KEY environment variable is required. Set it (setx) and restart Streamlit.")
    st.stop()

uploaded = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf","docx","txt"])

if uploaded:
    st.info("Extracting and cleaning text...")
    try:
        cleaned = extract_text(uploaded, save_to=None)
    except Exception as e:
        st.error(f"Extraction error: {e}")
        st.stop()
    safe_write_text("extracted_clean.txt", cleaned)
    st.success("Extraction complete")
    if st.checkbox("Preview extracted text"):
        st.text_area("Extracted (cleaned)", value=(cleaned[:20000]+"...") if len(cleaned)>20000 else cleaned, height=300)

    st.info("Sending text to Gemini for audiobook rewrite (this may take a while)...")
    try:
        rewritten = enrich_text(cleaned, use_gemini=True)
    except Exception as e:
        st.error(f"Gemini enrichment failed: {e}")
        st.stop()
    safe_write_text("enriched.txt", rewritten)
    st.success("Rewriting complete")
    if st.checkbox("Preview rewritten text"):
        st.text_area("Rewritten", value=(rewritten[:20000]+"...") if len(rewritten)>20000 else rewritten, height=300)

    # make audio-friendly: remove underscores and long dash sequences, collapse spaces
    audio_ready = rewritten.replace('_', ' ').replace('—', ' ').replace('–', ' ').replace('---', ' ')
    audio_ready = ' '.join(audio_ready.split())

    st.info("Chunking and synthesizing to WAV...")
    chunks = chunk_text_by_chars(audio_ready, max_chars=1800)
    st.write(f"{len(chunks)} chunks prepared.")

    tmpdir = tempfile.mkdtemp(prefix="audiobook_")
    wav_paths = []
    try:
        for i, ch in enumerate(chunks, start=1):
            st.write(f"Synthesizing chunk {i}/{len(chunks)}...")
            wav_path = Path(tmpdir) / f"chunk_{i}.wav"
            tts_save_pyttsx3(ch, str(wav_path))
            wav_paths.append(str(wav_path))

        final = Path(tmpdir) / "audiobook_final.wav"
        combine_wav_files(wav_paths, str(final))
        st.success("Audio generation complete")

        with open(final, "rb") as f:
            data = f.read()
        st.audio(data, format="audio/wav")
        st.download_button("Download audiobook (WAV)", data=data, file_name="audiobook_final.wav", mime="audio/wav")
    except Exception as e:
        st.error(f"Audio generation failed: {e}")
