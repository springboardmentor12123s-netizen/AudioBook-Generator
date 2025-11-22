import streamlit as st
import os
import json
import pyttsx3
import whisper

# Ensure output folders exist
os.makedirs("audio_uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# -----------------------------------------------------------
# Load Translations (English / Hindi)
# -----------------------------------------------------------
def load_language(lang):
    with open(f"translations/{lang}.json", "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------------------------------------
# Background Animation (CSS Gradient Animation)
# -----------------------------------------------------------
def set_gradient_background():
    gradient_css = """
    <style>
    body {
        background: linear-gradient(-45deg, #FFDEE9, #B5FFFC, #C7CEEA, #FF9CEE);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """
    st.markdown(gradient_css, unsafe_allow_html=True)

set_gradient_background()

# -----------------------------------------------------------
# Sidebar (Language + Navigation + Voice)
# -----------------------------------------------------------
st.sidebar.title("🌐 Language")
language = st.sidebar.selectbox("Choose Language", ["english", "hindi"])
T = load_language(language)

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to:", [T["nav_text_to_audio"], T["nav_song_to_lyrics"]])

st.sidebar.title("🎙 Voice")
voice_choice = st.sidebar.selectbox("Voice Type", ["Default", "Female", "Male"])

# -----------------------------------------------------------
# Main Page Layout
# -----------------------------------------------------------
st.markdown(
    f"<h1 style='text-align: center; color: #222;'>{T['app_title']}</h1>",
    unsafe_allow_html=True
)

# -----------------------------------------------------------
# Utility Functions (Free, Offline)
# -----------------------------------------------------------
def generate_speech(text, voice="Default"):
    """
    Generates speech from text using pyttsx3 and returns the output path
    """
    engine = pyttsx3.init()
    
    # Set voice
    voices = engine.getProperty('voices')
    if voice.lower() == "female" and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    elif voice.lower() == "male":
        engine.setProperty('voice', voices[0].id)

    output_path = os.path.join("outputs", "audiobook.mp3")
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path

def extract_lyrics_from_audio(audio_path):
    """
    Extracts lyrics / text from audio using OpenAI Whisper
    """
    model = whisper.load_model("base")  # Works offline
    result = model.transcribe(audio_path)
    return result["text"]

# -----------------------------------------------------------
# PAGE 1 — TEXT / PDF → AUDIOBOOK
# -----------------------------------------------------------
if page == T["nav_text_to_audio"]:
    st.subheader(T["subtitle_text_to_audio"])

    option = st.radio(T["choose_input_type"], [T["upload_pdf"], T["enter_text"]])

    extracted_text = ""

    # -------- PDF Upload --------
    if option == T["upload_pdf"]:
        from utils.file_utils import extract_text_from_pdf
        pdf_file = st.file_uploader(T["upload_pdf_prompt"], type=["pdf"])
        if pdf_file:
            pdf_path = os.path.join("audio_uploads", pdf_file.name)
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            extracted_text = extract_text_from_pdf(pdf_path)
            extracted_text = extracted_text.strip()
            st.text_area(T["extracted_text"], extracted_text, height=250)

    # -------- Manual Text Entry --------
    else:
        extracted_text = st.text_area(T["enter_text_prompt"], height=250)

    # -------- Generate Audiobook --------
    if st.button(T["generate_audio_btn"]):
        if extracted_text.strip() == "":
            st.error(T["error_no_text"])
        else:
            st.info(T["audio_generating"])
            output_path = generate_speech(extracted_text, voice_choice)

            with open(output_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label=T["download_audio"],
                data=audio_bytes,
                file_name="audiobook.mp3",
                mime="audio/mp3"
            )

# -----------------------------------------------------------
# PAGE 2 — SONG → LYRICS EXTRACTION
# -----------------------------------------------------------
elif page == T["nav_song_to_lyrics"]:
    st.subheader(T["subtitle_song_to_lyrics"])

    song_file = st.file_uploader(T["upload_song_prompt"], type=["mp3", "wav", "m4a"])

    if song_file:
        song_path = os.path.join("audio_uploads", song_file.name)
        with open(song_path, "wb") as f:
            f.write(song_file.getbuffer())

        st.success(T["audio_uploaded"])

        if st.button(T["extract_lyrics_btn"]):
            st.info(T["extracting_lyrics"])
            lyrics = extract_lyrics_from_audio(song_path)
            lyrics = lyrics.strip()

            st.text_area(T["lyrics_output"], lyrics, height=300)
            st.download_button(
                label=T["download_lyrics"],
                data=lyrics,
                file_name="lyrics.txt",
                mime="text/plain"
            )

