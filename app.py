# app.py
import streamlit as st
import os
from core.extractor import extract_texts
from core.groqres import generate_script
from core.audiogen import text_to_speech

# --------- Page config ----------
st.set_page_config(page_title="AI Audiobook Generator", page_icon="🎧")
st.title("🎧 AI Audiobook Generator — Week 1")

# --------- Session state keys ----------
if "script" not in st.session_state:
    st.session_state.script = None

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

# --------- File uploader ----------
File_type = st.selectbox(
    "Select the type of file you want to upload:",
    ["PDF", "DOCX", "TXT"]
)

uploaded_files = st.file_uploader(
    "Upload any PDF/DOCX/TXT files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

text_extracted = {}
if uploaded_files:
    st.subheader("Extracted Text Preview")
    text_extracted = extract_texts(uploaded_files)
    for name, text in text_extracted.items():
        st.write(f"**{name}**")
        preview = (text[:2000] + "...") if len(text) > 2000 else text
        st.code(preview or "[No text extracted]")
else:
    st.info("Upload a file to begin.")

# --------- Generate script ----------
if text_extracted:
    user_prompt = st.text_area("Enter custom narration / instructions (optional)", height=120)

    if st.button("Generate Audiobook Script"):
        with st.spinner("Generating audiobook script..."):
            full_input = str(user_prompt) + "\n" + str(text_extracted)
            try:
                st.session_state.script = generate_script(full_input)
                st.success("Script generated successfully!")
                # Clear any previous audio so user explicitly regenerates audio
                st.session_state.audio_file = None
            except Exception as e:
                st.error(f"Script generation failed: {e}")

# --------- Show script ----------
if st.session_state.script:
    st.subheader("Generated Audiobook Script")
    st.code(st.session_state.script)

    # Generate audio button (only visible when script exists)
    if st.button("🎧 Generate Audio"):
        with st.spinner("Generating audio... this may take a few seconds"):
            try:
                saved_path = text_to_speech(st.session_state.script)
                st.session_state.audio_file = saved_path
                st.success(f"Audio generated successfully and saved to:\n{saved_path}")
            except Exception as e:
                st.error(f"Audio generation failed: {e}")
                st.info("Make sure gTTS is installed (`pip install gTTS`) and you have internet access.")

# --------- Play & download (only if audio exists) ----------
if st.session_state.audio_file:
    audio_path = st.session_state.audio_file
    if os.path.exists(audio_path):
        st.subheader("🔊 Your Audiobook")

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        # Play inside Streamlit
        st.audio(audio_bytes, format="audio/mp3")

        # Download button
        st.download_button(
            label="📥 Download Audiobook",
            data=audio_bytes,
            file_name=os.path.basename(audio_path),
            mime="audio/mpeg"
        )
    else:
        st.error(f"Expected audio file at {audio_path} but file not found.")
        st.session_state.audio_file = None
