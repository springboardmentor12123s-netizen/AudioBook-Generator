import streamlit as st
from text_extraction import extract_text
from llm_enrichment import enrich_text_for_audio
from tts_generator import generate_audiobook

st.title("AI Audiobook Generator")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")
    raw_text = extract_text(uploaded_file.name)
    st.text_area("Extracted Text Preview", raw_text[:])

    if st.button("Generate Audiobook "):
        with st.spinner("Enhancing text using Gemini..."):
            enriched_text = enrich_text_for_audio(raw_text)
        with st.spinner("Converting text to audio..."):
            audio_path = generate_audiobook(enriched_text)
        st.success("Audiobook ready!")
        st.audio(audio_path, format="audio/wav")
        with open(audio_path, "rb") as audio_file:
            st.download_button("Download Audiobook", audio_file, file_name="audiobook.wav")
