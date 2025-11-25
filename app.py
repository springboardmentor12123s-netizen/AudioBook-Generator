import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document
from num2words import num2words
import re
import google.generativeai as genai
from gtts import gTTS

# Supported languages 
SUPPORTED_LANGUAGES = {
    "English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr",
    "German": "de", "Italian": "it", "Portuguese": "pt", "Russian": "ru",
    "Arabic": "ar", "Chinese (Simplified)": "zh", "Japanese": "ja", "Korean": "ko"
}

# Load API keys
load_dotenv(".env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI API key not found. Add GEMINI_API_KEY to .env")
    st.stop()

# Configure Gemini 
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Helper Functions
def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return " ".join([p.text for p in doc.paragraphs])
    else:
        st.error("Unsupported file type.")
        return ""

def grammar_correction(text):
    st.info("⏳ Sending text to Gemini for correction...")
    if len(text) > 30000:
        text = text[:30000]
        st.warning("Text truncated to 30000 chars")
    prompt = f"""
    You are a writing assistant. Correct grammatical errors and improve readability.
    Return only the improved text.
    Text:
    {text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return "Error: Could not generate response."

def translate_text(text, target_language_code):
    prompt = f"""
    Translate the following text into language code '{target_language_code}'.
    Return ONLY the translated text.
    Text:
    {text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Translation Error: {e}")
        return text

def text_to_speech(text, lang="en", output_path="output_audio.mp3"):
    """Convert text to speech using gTTS."""
    # Convert numbers to words
    text = re.sub(r'\b\d+\b', lambda m: num2words(int(m.group())), text)

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)
        return output_path
    except Exception as e:
        st.error(f"gTTS Error: {e}")
        return None

# Streamlit UI 
st.title("🎧 Grammar-Correcting Multi-Language AudioBook Generator")

uploaded_file = st.file_uploader("Upload a text, PDF, or Word document", type=["txt", "pdf", "docx"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        raw_text = extract_text(uploaded_file)
    if not raw_text.strip():
        st.error("File is empty or could not be extracted.")
        st.stop()

    st.subheader("Original Extracted Text")
    st.text_area("Raw text:", raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text, height=200)

    st.subheader("🌍 Output Language Selection")
    selected_language = st.selectbox("Choose the output language:", list(SUPPORTED_LANGUAGES.keys()))
    target_code = SUPPORTED_LANGUAGES[selected_language]

    if st.button("Process and Generate Audio"):
        # Grammar Correction
        with st.spinner("Correcting text..."):
            corrected_text = grammar_correction(raw_text)

        st.subheader("Corrected Text")
        st.text_area("Clean version:", corrected_text, height=250)

        # Generate audio (original)
        with st.spinner("Generating audio (original)..."):
            audio_path = text_to_speech(corrected_text, lang="en", output_path="audio_original.mp3")
        if audio_path:
            st.success("Audio generated!")
            st.audio(audio_path)
            with open(audio_path, "rb") as f:
                st.download_button("Download Audio", f, file_name="audio_original.mp3")

        # Translation
        with st.spinner(f"Translating to {selected_language}..."):
            translated_text = translate_text(corrected_text, target_code)

        st.subheader(f"Translated Text ({selected_language})")
        st.text_area("Translated version:", translated_text, height=250)

        # Generate audio (translated)
        with st.spinner(f"Generating audio in {selected_language}..."):
            translated_audio_path = text_to_speech(translated_text, lang=target_code, output_path=f"audio_{target_code}.mp3")
        if translated_audio_path:
            st.success(f"Audio generated in {selected_language}!")
            st.audio(translated_audio_path)
            with open(translated_audio_path, "rb") as f:
                st.download_button(f"Download {selected_language} Audio", f, file_name=f"audio_{target_code}.mp3")
