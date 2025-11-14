import streamlit as st
from core.extractor import extract_text
from core.enrich_text import enrich_text
from core.generate_audio import create_audio

st.title("📚 AI Audiobook Generator")
st.write("Upload PDF, DOCX or TXT → Enhance with AI → Convert to Audiobook")

# Session state storage
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""

if "enriched_text" not in st.session_state:
    st.session_state.enriched_text = ""


uploaded_file = st.file_uploader("Upload File", type=["pdf","docx","txt"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]
    st.success("File uploaded successfully!")

    # Extract Text Button
    if st.button("Extract Text"):
        st.session_state.raw_text = extract_text(uploaded_file, file_type)

    # Show extracted text
    if st.session_state.raw_text:
        st.text_area("Extracted Text", st.session_state.raw_text[:3000], height=250)

        # Enhance Button
        if st.button("Enhance for Audiobook Narration"):
            st.session_state.enriched_text = enrich_text(st.session_state.raw_text)

    # Show enhanced text
    if st.session_state.enriched_text:
        st.text_area("Enhanced Audiobook Text", st.session_state.enriched_text[:3000], height=250)

        # Generate Audio Button
        if st.button("Generate Audio"):
            with st.spinner("Generating audio... Please wait..."):
                audio_file = create_audio(st.session_state.enriched_text)

                # Read audio file
                with open(audio_file, "rb") as audio:
                    audio_bytes = audio.read()

                st.success("Audio generated successfully!")

                # AUDIO PLAYER — listen inside the app
                st.audio(audio_bytes, format="audio/mp3")

                # DOWNLOAD BUTTON
                st.download_button(
                    label="Download Audiobook",
                    data=audio_bytes,
                    file_name="audiobook.mp3",
                    mime="audio/mp3"
                )