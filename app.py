import streamlit as st
from core.extractors import extract_text_from_file
from core.llm import enrich_text_with_llm
from core.tts import text_to_speech
from core.utils import split_text_for_tts, safe_filename
import os
from io import BytesIO

# Streamlit page settings
st.set_page_config(page_title="🎧 AudioBook Generator", layout="wide")
# Load custom CSS for styling
with open("assets/styles.css", "r") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Page title & subtitle
st.markdown("<h1 class='title'>🎧 AudioBook Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Convert PDF, DOCX, and TXT files into high-quality audiobooks.</p>", unsafe_allow_html=True)

# File upload
uploaded_files = st.file_uploader("📂 Upload files", accept_multiple_files=True, type=['pdf', 'docx', 'txt'])

# Language selection
lang = st.selectbox("🌐 Audio Language", ["English (en)", "Hindi (hi)"])
language_code = "en" if "English" in lang else "hi"

# Optional AI enhancement
use_llm = st.checkbox("✨ Enhance narration with AI")

# Main processing
if st.button("Generate Audiobook 🎶"):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one file.")
        st.stop()

    # Create temp folder for audio output
    os.makedirs("temp_audio", exist_ok=True)
    combined_text = ""

    # Extract text from uploaded files
    st.info("📄 Extracting text from files...")
    for file in uploaded_files:
        st.write(f"✔️ Processing: **{file.name}**")
        combined_text += "\n\n" + extract_text_from_file(file)

    # Apply AI enhancement if enabled
    if use_llm:
        st.info("🧠 Enhancing content using AI...")
        combined_text = enrich_text_with_llm(combined_text)

    # Split text into chunks suitable for TTS
    chunks = split_text_for_tts(combined_text, 2500)
    st.info(f"🔊 Generating {len(chunks)} audio segments...")

    mp3_paths = []

    # Convert each chunk to audio
    for i, chunk in enumerate(chunks):
        output_path = f"temp_audio/part_{i+1}.mp3"
        text_to_speech(chunk, lang=language_code, out_path=output_path)
        mp3_paths.append(output_path)

    # Merge all MP3 parts into one output file
    final_mp3 = "temp_audio/audiobook_final.mp3"
    with open(final_mp3, "wb") as f:
        for p in mp3_paths:
            f.write(open(p, "rb").read())

    # Display and download audio
    st.success("🎉 Audiobook generated successfully!")
    st.audio(final_mp3)

    with open(final_mp3, "rb") as f:
        st.download_button("⬇️ Download Audiobook", f, "audiobook.mp3", "audio/mpeg")
