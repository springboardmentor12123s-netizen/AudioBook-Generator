# app_streamlit_final.py
import os
import tempfile
import streamlit as st
from pathlib import Path

# imports from your modules
from pymod.text_extraction import extract_text
from pymod.llm import enrich_text
# single-file TTS function expected in modules/tts_engine.py
from pymod.text2spe import synthesize_text_to_single_file
from pymod.utils import safe_write_text

st.set_page_config(page_title="AI AudioBook Generator", layout="wide")
st.title("🎧 AI AudioBook Generator (Single-file TTS, with pyttsx3 fallback)")

# --- Sidebar: API key input and TTS method selection
if "GEMINI_KEY_PASTE" not in st.session_state:
    st.session_state["GEMINI_KEY_PASTE"] = ""

key_in_app = st.sidebar.text_input("Paste MakerSuite API key (optional)", type="password", value=st.session_state["GEMINI_KEY_PASTE"])
if key_in_app:
    os.environ["GEMINI_API_KEY"] = key_in_app
    st.session_state["GEMINI_KEY_PASTE"] = key_in_app

tts_method = st.sidebar.selectbox("Preferred TTS method (gtts recommended)", ["gtts", "pyttsx3"])
st.sidebar.info("gTTS = faster, needs internet. pyttsx3 = offline, may be slower on Windows.")

if not os.environ.get("GEMINI_API_KEY"):
    st.sidebar.warning("GEMINI_API_KEY not found. Paste the key here or set env var before using Gemini.")

# Ensure session_state variables exist
for k in ("extracted", "enriched", "audio_bytes", "last_uploaded_name", "last_audio_path"):
    if k not in st.session_state:
        st.session_state[k] = None

uploaded = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf", "docx", "txt"])
col1, col2 = st.columns([1, 1])

# Handle upload and extraction
if uploaded is not None:
    # If a new file uploaded, clear previous enriched/audio
    if st.session_state["last_uploaded_name"] != uploaded.name:
        st.session_state["extracted"] = None
        st.session_state["enriched"] = None
        st.session_state["audio_bytes"] = None
        st.session_state["last_audio_path"] = None
        st.session_state["last_uploaded_name"] = uploaded.name

    with st.spinner("Extracting text..."):
        try:
            extracted = extract_text(uploaded)
            # small cleaning step and save
            safe_write_text("extracted_clean.txt", extracted)
            st.session_state["extracted"] = extracted
            st.success("Extraction complete.")
        except Exception as e:
            st.error(f"Extraction failed: {e}")
            st.stop()

# Left column: extracted text
col1.subheader("Extracted (cleaned)")
if st.session_state["extracted"]:
    col1.text_area("extracted", value=(st.session_state["extracted"][:20000] + "...") if len(st.session_state["extracted"]) > 20000 else st.session_state["extracted"], height=300)
else:
    col1.info("Upload a file to extract text.")

# Right column: enrichment UI + TTS controls
col2.subheader("Rewritten (enriched) & TTS")

# Button: Rewrite with Gemini
if st.button("Rewrite with Gemini"):
    if not st.session_state["extracted"]:
        st.error("No extracted text found. Upload and extract first.")
    else:
        with st.spinner("Rewriting with Gemini (this may take some time)..."):
            try:
                enriched = enrich_text(st.session_state["extracted"], use_gemini=True)
                st.session_state["enriched"] = enriched
                safe_write_text("enriched.txt", enriched)
                st.success("Rewrite complete — see right panel.")
            except Exception as e:
                st.session_state["enriched"] = None
                st.error(f"Gemini failed: {e}")

# Show enriched if exists
if st.session_state["enriched"]:
    col2.text_area("enriched", value=(st.session_state["enriched"][:20000] + "...") if len(st.session_state["enriched"]) > 20000 else st.session_state["enriched"], height=300)
else:
    col2.info("No enriched text yet. Click 'Rewrite with Gemini' to generate.")

# Button: Generate Audiobook (only shown if enriched exists)
if st.session_state["enriched"]:
    if st.button("Generate Audiobook (TTS)"):
        with st.spinner("Generating audio (may take 10-60s depending on method)..."):
            tmpdir = tempfile.mkdtemp(prefix="audiobook_")
            # prefer gTTS unless user selected pyttsx3
            primary = "pyttsx3" if tts_method == "pyttsx3" else "gtts"
            try:
                final_path = synthesize_text_to_single_file(st.session_state["enriched"], tmpdir, out_name="audiobook_final", method=primary)
            except Exception as e_primary:
                st.warning(f"{primary} failed: {e_primary}. Trying fallback method...")
                fallback = "pyttsx3" if primary == "gtts" else "gtts"
                try:
                    final_path = synthesize_text_to_single_file(st.session_state["enriched"], tmpdir, out_name="audiobook_final", method=fallback)
                except Exception as e_fallback:
                    st.error(f"Both TTS methods failed. Primary error: {e_primary}; Fallback error: {e_fallback}")
                    final_path = None

            if final_path:
                try:
                    audio_bytes = Path(final_path).read_bytes()
                    st.session_state["audio_bytes"] = audio_bytes
                    st.session_state["last_audio_path"] = final_path
                    st.success("Audio generation complete.")
                except Exception as e:
                    st.error(f"Failed to read generated audio file: {e}")

# If audio available, show player & download
if st.session_state["audio_bytes"]:
    col2.audio(st.session_state["audio_bytes"], format="audio/wav")
    # choose filename based on uploaded name
    base_name = (st.session_state["last_uploaded_name"] or "audiobook").rsplit(".", 1)[0]
    download_name = f"{base_name}_audiobook.wav"
    col2.download_button("Download WAV", data=st.session_state["audio_bytes"], file_name=download_name, mime="audio/wav")

# Footer: small status
st.write("---")
st.write("Status:")
st.write(f"- Extracted: {'Yes' if st.session_state['extracted'] else 'No'}")
st.write(f"- Enriched: {'Yes' if st.session_state['enriched'] else 'No'}")
st.write(f"- Audio generated: {'Yes' if st.session_state['audio_bytes'] else 'No'}")
if st.session_state.get("last_audio_path"):
    st.write(f"- Last audio file: {st.session_state['last_audio_path']}")
