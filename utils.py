# utils.py
# Handles Text Extraction, Translation, and TTS

import streamlit as st
import PyPDF2
from docx import Document
from gtts import gTTS
import pyttsx3
import io
import os
from deep_translator import GoogleTranslator # The new reliable translator

def extract_text(uploaded_file):
    """Extracts text from PDF, DOCX, or TXT."""
    try:
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        elif uploaded_file.type == "text/plain":
            return uploaded_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

def translate_text(text, target_lang_code):
    """
    Translates text to the target language using Deep Translator.
    This is much more reliable than using an LLM.
    """
    try:
        # GoogleTranslator limits text length (approx 5000 chars), so we split it if needed.
        # For simplicity in this example, we treat it as one block, but deep_translator handles standard chunks well.
        translator = GoogleTranslator(source='auto', target=target_lang_code)
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation Error: {e}")
        return text # Return original text if translation fails

def convert_text_to_speech_gtts(text, lang='en'):
    """Online TTS using Google Text-to-Speech (Supports Telugu, Hindi, etc.)"""
    try:
        # gTTS expects 'te' for Telugu, 'hi' for Hindi, etc.
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        st.error(f"gTTS Error: {e}")
        return None

def convert_text_to_speech_pyttsx3(text):
    """Offline TTS (Mostly English, depends on system voices)"""
    try:
        engine = pyttsx3.init()
        temp_filename = "temp_audio_offline.mp3"
        engine.save_to_file(text, temp_filename)
        engine.runAndWait()
        
        audio_fp = io.BytesIO()
        with open(temp_filename, "rb") as f:
            audio_fp.write(f.read())
        
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        st.error(f"pyttsx3 Error: {e}")
        return None