# AudioBook Generator

**Author:** Jeeval Shah  
**Target Audience:** Individuals with visual impairments or those who prefer auditory learning.  

## Overview
AudioBook Generator is a Streamlit-based application that converts documents and written text into natural-sounding speech using ElevenLabs’ text-to-speech API.  
The tool enhances accessibility by allowing visually impaired users to listen to content such as PDFs, Word files, or plain text — turning reading into an effortless listening experience.

---

## Features
- Multi-format support: Upload `.pdf`, `.docx`, or `.txt` files  
- Realistic AI voice generation with ElevenLabs  
- Option to download generated audio in `.mp3` format  
- Automatic text cleaning and formatting  
- Simple, user-friendly Streamlit interface  

---

## Tech Stack
- **Frontend/UI:** Streamlit  
- **Text-to-Speech Engine:** ElevenLabs API  
- **Text Processing:** NLTK, PyPDF2, python-docx  
- **Backend Language:** Python  
- **Environment:** `.env` for API key management  

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/springboardmentor12123s-netizen/AudioBook-Generator.git
cd AudioBook-Generator
```

### 2. Create a virtual environment

```bash
conda create -n 'Audiobook' python=3.13
conda activate Audiobook
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add ElevenLabs & Gemini API KEY in .env
```bash
GEMINI_API_KEY=your_gemini_api_key_here
ELEVEN_API_KEY=your_elevenlabs_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```