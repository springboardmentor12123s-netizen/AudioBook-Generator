# Audiobook  Generator

A modern Streamlit web app that converts text or PDF files into audiobooks and extracts clean lyrics from any song.  
The project includes multilingual UI support (English + Hindi), audio processing, PDF text extraction, and a beautiful animated frontend.

---

## Features

1. Text to Audiobook
   - Upload a PDF or paste text
   - Extract text automatically
   - Convert text into MP3 audiobook using OpenAI TTS
   - Download the generated audio file

2. Song to Lyrics
   - Upload any song (MP3/WAV)
   - Extract lyrics using Google Speech-to-Text API
   - Automatic cleanup of text, removing noise or timestamps
   - Download lyrics as a text file

3. Multilingual Support
   - Switch between English and Hindi UI
   - All labels and messages updated instantly

4. Beautiful UI
   - Animated background
   - Frosted glass card effects
   - Modern fonts
   - Smooth animations

---

## Tech Stack

Frontend:
- Streamlit
- Custom CSS

Backend:
- OpenAI Text-to-Speech API
- Google Cloud Speech-to-Text API
- PyPDF2 (PDF text extraction)
- Pydub (audio processing)

Project Structure:

The app will open automatically in your browser.

---

## How It Works

1. Audiobook Generation:
   - If PDF uploaded → text is extracted using PyPDF2
   - If text entered → taken directly from user input
   - Sent to OpenAI TTS model
   - MP3 file is generated and available for download

2. Song Lyrics Extraction:
   - User uploads an MP3/WAV file
   - Processed with Pydub
   - Google Speech-to-Text converts audio to words
   - Script cleans lyrics (removes timestamps, noise, spacing)
   - Clean lyrics displayed and downloadable

3. Multilingual UI:
   - All UI text comes from english.json or hindi.json
   - When language selected → app loads corresponding file

---

## Requirements

See requirements.txt:
streamlit
pydub
openai
PyPDF2
google-cloud-speech
google-cloud-storage
google-cloud-language

