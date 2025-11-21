import streamlit as st
import os
from elevenlabs import ElevenLabs

import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document

from num2words import num2words
import re

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Chinese (Simplified)": "zh",
    "Japanese": "ja",
    "Korean": "ko"
}

load_dotenv(dotenv_path=".env")  
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI API key not found. Please add it to a .env file as GEMINI_API_KEY=your_key_here.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

def extract_text(file):
    """Extract text from uploaded file (txt, pdf, docx)."""
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
    """Use Gemini to correct grammar and clarity."""
    st.info("⏳ Sending text to Gemini for correction...")
    
    # Limit length to avoid API timeout
    if len(text) > 30000:
        text = text[:30000]
        st.warning("Text truncated to 30000 characters for faster response.")
    
    prompt = f"""
        You are a writing assistant. Please correct any grammatical errors and improve the readability of the following text. 
        Do not add any introductory phrases (like "Here's the corrected version") or explanations. 
        Return only the improved text itself, without any formatting symbols such as ** or markdown syntax.

        Text:
        {text}
        """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return "Error: Could not generate response."

def text_to_speech(text, output_path="output_audio.mp3"):
    """Convert text to natural speech using ElevenLabs (v1 SDK)."""
    
    # Convert numbers to words
    def convert_numbers(match):
        num = match.group()
        try:
            return num2words(int(num))
        except:
            return num

    text = re.sub(r'\b\d+\b', convert_numbers, text)

    eleven_key = os.getenv("ELEVEN_API_KEY")
    if not eleven_key:
        raise ValueError("ELEVEN_API_KEY not found in .env")

    # Initialize ElevenLabs client
    client = ElevenLabs(api_key=eleven_key)

    # Generate audio with a natural voice
    audio = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Rachel (female)
        model_id="eleven_multilingual_v2",
        text=text
    )

    # Save the audio output
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path

def translate_text(text, target_language_code):
    """Translate text to any target language using Gemini."""

    prompt = f"""
    Translate the following text into the language represented by code '{target_language_code}'.
    Return ONLY the translated text. No quotes, no explanations, no formatting, no labels.

    Text:
    {text}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Translation Error: {e}")
        return text


st.title("🎧 Grammar-Correcting AudioBook Generator (Prototype)")

uploaded_file = st.file_uploader("Upload a text, PDF, or Word document", type=["txt", "pdf", "docx"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        raw_text = extract_text(uploaded_file)

    if not raw_text.strip():
        st.error("The uploaded file appears to be empty or could not be extracted.")
        st.stop()

    st.subheader("Original Extracted Text")
    st.text_area("Raw text:", raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text, height=200)

    st.subheader("🌍 Output Language Selection")
    selected_language = st.selectbox(
        "Choose the output language for final audio:",
        list(SUPPORTED_LANGUAGES.keys())
    )

    st.info("This may take 10–30 seconds for large documents...")
    
    if st.button("Process and Generate Audio"):
        with st.spinner("Preprocessing and correcting text..."):
            corrected_text = grammar_correction(raw_text)

        st.subheader("Corrected Text")
        st.text_area("Clean version:", corrected_text, height=250)

        # Step 1: Generate initial TTS (original language)
        with st.spinner("Generating audio (original language)..."):
            audio_path_original = text_to_speech(corrected_text)

        st.success("Original language audio generated!")
        st.audio(audio_path_original)

        with open(audio_path_original, "rb") as f:
            st.download_button("Download Original Audio", f, file_name="audio_original.mp3")

        # Step 2: Translate into selected language
        target_code = SUPPORTED_LANGUAGES[selected_language]

        with st.spinner(f"Translating into {selected_language}..."):
            translated_text = translate_text(corrected_text, target_code)

        st.subheader(f"Translated Text ({selected_language})")
        st.text_area("Translated version:", translated_text, height=250)

        # Step 3: Generate TTS for translated text
        with st.spinner(f"Generating audio in {selected_language}..."):
            translated_audio_path = text_to_speech(
                translated_text,
                output_path=f"audio_{target_code}.mp3"
            )

        st.success(f"Audio generated in {selected_language}!")
        st.audio(translated_audio_path)

        with open(translated_audio_path, "rb") as f:
            st.download_button("Download Translated Audio", f, file_name="audio_translated.mp3")


