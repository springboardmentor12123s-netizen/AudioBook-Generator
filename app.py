import streamlit as st
from services.audio_services import generate_speech
from utils.lyrics_extractor import extract_lyrics_from_audio
from utils.file_utils import extract_text_from_file, save_uploaded_file
from utils.summarizer import summarize_text
from utils.translator import translate_text

# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="Audiobook Generator",
    page_icon="🎧",
    layout="centered"
)

page_bg = """
<style>
.stApp {
    background: linear-gradient(120deg, #0f0f29, #1b1b3a, #10101e);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    color: #ffffff;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🎧 Audiobook Generator</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📄 Text → Audio", "📁 File → Audio", "🎵 Audio → Lyrics"])

# ===================================================
# 1) TEXT → AUDIOBOOK TAB
# ===================================================
with tab1:
    st.subheader("Convert text into an audiobook")

    user_text = st.text_area("Enter text", height=200)
    voice = st.selectbox("Choose voice", ["male", "female"])
    lang = st.selectbox("Output Language", ["English", "Hindi"])
    do_summary = st.checkbox("Summarize before converting?")

    if st.button("Generate Audiobook"):
        if not user_text.strip():
            st.error("Please enter text.")
        else:
            if do_summary:
                user_text = summarize_text(user_text)

            if lang == "Hindi":
                user_text = translate_text(user_text, target_lang="hi")

            audio_file = generate_speech(user_text, voice)

            st.audio(audio_file)
            st.download_button("Download MP3", audio_file, file_name="audiobook.mp3")
            st.success("Audiobook generated successfully!")


# ===================================================
# 2) FILE → AUDIOBOOK TAB
# ===================================================
with tab2:
    st.subheader("Upload a PDF / DOCX / TXT and convert to audio")

    file = st.file_uploader("Upload file", type=["pdf", "docx", "txt"])
    voice = st.selectbox("Choose voice", ["male", "female"], key="file_voice")
    lang = st.selectbox("Output Language", ["English", "Hindi"], key="file_lang")
    do_summary_file = st.checkbox("Summarize extracted text?")

    if st.button("Convert File to Audio"):
        if file is None:
            st.error("Please upload a file.")
        else:
            saved_path = save_uploaded_file(file)
            extracted_text = extract_text_from_file(saved_path)

            if do_summary_file:
                extracted_text = summarize_text(extracted_text)

            if lang == "Hindi":
                extracted_text = translate_text(extracted_text, target_lang="hi")

            audio_file = generate_speech(extracted_text, voice)

            st.audio(audio_file)
            st.download_button("Download MP3", audio_file, file_name="file_audio.mp3")
            st.success("Conversion completed!")


# ===================================================
# 3) AUDIO → LYRICS TAB
# ===================================================
with tab3:
    st.subheader("Upload an audio file to extract lyrics")

    audio_file_upload = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])

    if st.button("Extract Lyrics"):
        if audio_file_upload is None:
            st.error("Please upload an audio file.")
        else:
            audio_path = save_uploaded_file(audio_file_upload)
            lyrics = extract_lyrics_from_audio(audio_path)

            st.text_area("Extracted Lyrics", lyrics, height=300)
            st.success("Lyrics extracted!")
