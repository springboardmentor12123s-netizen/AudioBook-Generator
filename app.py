import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables (auto-find .env) BEFORE other imports
load_dotenv(find_dotenv())

from text_extraction import extract_text
from llm_enrichment import enrich_text_for_audio
from tts_generator import generate_audiobook

st.title("🎧 AI Audiobook Generator")

if not os.getenv("GEMINI_API_KEY"):
    st.error("⚠️ GEMINI_API_KEY is missing. Please add it to your .env file.")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Save to disk to read with other libs
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File uploaded successfully!")
    try:
        raw_text = extract_text(uploaded_file.name)
        st.text_area("📜 Extracted Text Preview", raw_text[:1000])

        if st.button("Generate Audiobook 🎙️"):
            with st.spinner("Enhancing text using Gemini..."):
                enriched_text = enrich_text_for_audio(raw_text)
            with st.spinner("Converting text to audio..."):
                audio_path = generate_audiobook(enriched_text)
            
            if audio_path and os.path.exists(audio_path):
                st.success("🎧 Audiobook ready!")
                
                # Open as binary to avoid Streamlit file path issues
                with open(audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                
                st.audio(audio_bytes, format="audio/wav")
                
                st.download_button("Download Audiobook", audio_bytes, file_name="audiobook.wav", mime="audio/wav")
            else:
                st.error("❌ Audio generation failed.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
