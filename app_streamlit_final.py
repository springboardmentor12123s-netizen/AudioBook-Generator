import streamlit as st
import os
from dotenv import load_dotenv

from pymod.text_extraction import extract_text
from pymod.llm import enrich_and_translate_text
from pymod.text2spe import synthesize_text_to_single_file, LANGUAGE_MAP

# Load environment variables silently
load_dotenv(override=True)

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Audiobook Studio",
    page_icon="🎧",
    layout="centered"
)

# -------------------- HEADER --------------------
st.markdown(
    """
    <h1 style="text-align:center;">🎧 AI Audiobook Studio</h1>
    <p style="text-align:center; font-size:16px;">
        Convert documents into polished, multilingual audiobooks using Generative AI
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# -------------------- SESSION STATE --------------------
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = None

if "final_text" not in st.session_state:
    st.session_state.final_text = None

if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# -------------------- LANGUAGE SELECTION --------------------
st.subheader("🌍 Select Audio Language")

language_label = st.selectbox(
    "Choose the language for rewriting, translation, and narration",
    list(LANGUAGE_MAP.keys()),
    index=0
)

language_code = LANGUAGE_MAP[language_label]

st.markdown("---")

# -------------------- FILE UPLOAD --------------------
st.subheader("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF or TXT file",
    type=["pdf", "txt"]
)

# -------------------- TEXT EXTRACTION --------------------
if uploaded_file:
    if st.button("📘 Extract Text"):
        with st.spinner("Extracting text from document..."):
            try:
                extracted = extract_text(uploaded_file)
                st.session_state.extracted_text = extracted
                st.success("Text extracted successfully")
            except Exception as e:
                st.error(f"Extraction failed: {e}")

# -------------------- SHOW EXTRACTED TEXT --------------------
if st.session_state.extracted_text:
    st.subheader("📝 Extracted Text (Cleaned)")
    st.text_area(
        label="",
        value=st.session_state.extracted_text,
        height=200
    )

    st.markdown("---")

    # -------------------- REWRITE / TRANSLATE --------------------
    st.subheader("🤖 Enhance with Gemini")

    process_mode = st.selectbox(
        "Processing mode",
        [
            "Rewrite & Translate (Recommended)",
            "Rewrite Only",
            "Skip Enhancement"
        ]
    )

    if st.button("✨ Process Text"):
        with st.spinner("Processing with Gemini AI..."):
            try:
                if process_mode == "Skip Enhancement":
                    st.session_state.final_text = st.session_state.extracted_text
                else:
                    st.session_state.final_text = enrich_and_translate_text(
                        text=st.session_state.extracted_text,
                        target_language=language_label,
                        rewrite_only=(process_mode == "Rewrite Only")
                    )

                st.success("Text processed successfully")

            except Exception as e:
                st.error(f"Gemini processing failed: {e}")

# -------------------- SHOW FINAL TEXT --------------------
if st.session_state.final_text:
    st.subheader("✅ Final Text Used for Audio")
    st.text_area(
        label="",
        value=st.session_state.final_text,
        height=220
    )

    st.markdown("---")

    # -------------------- AUDIO GENERATION --------------------
    st.subheader("🎙️ Generate Audiobook")

    if st.button("🔊 Generate Audio"):
        with st.spinner("Generating audiobook..."):
            try:
                output_dir = "output_audio"
                audio_file = synthesize_text_to_single_file(
                    text=st.session_state.final_text,
                    out_dir=output_dir,
                    out_name="audiobook_final",
                    lang=language_code
                )

                st.session_state.audio_path = audio_file
                st.success("Audiobook generated successfully")

            except Exception as e:
                st.error(f"Audio generation failed: {e}")

# -------------------- AUDIO PLAYER & DOWNLOAD --------------------
if st.session_state.audio_path:
    st.subheader("🎧 Listen & Download")

    st.audio(st.session_state.audio_path)

    with open(st.session_state.audio_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Audiobook",
            data=f,
            file_name=os.path.basename(st.session_state.audio_path),
            mime="audio/wav"
        )

    st.markdown("---")

# -------------------- FOOTER --------------------
st.markdown(
    """
    <div style="text-align:center; font-size:13px; color:gray;">
        Built with ❤️ using Streamlit, Gemini AI, and gTTS<br>
        Infosys Springboard Project
    </div>
    """,
    unsafe_allow_html=True
)
