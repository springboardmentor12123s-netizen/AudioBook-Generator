# 🎧 AudioBook Generator

A Streamlit-based application that converts **PDF, DOCX, and TXT** files into **multilingual audiobooks** with optional AI text rewriting and translation.

---

## 🚀 Features

### 📄 1. Fast Document Extraction
- PDF extraction using **PyMuPDF** (fast + accurate)
- DOCX extraction with `python-docx`
- TXT extraction with UTF-8 decoding
- Quick preview mode for faster performance

---

### 📝 2. Optional Text Rewriting

#### **Local Quick Rewrite (Offline)**
- No API required  
- Breaks long sentences  
- Improves narration flow  

#### **Gemini Rewrite (Cloud)**
- Uses Google Gemini models  
- Quota-safe:
  - Retry delay handling  
  - Backoff strategy  
  - Local fallback on quota exceed  

---

### 🌍 3. Translation Before TTS
Convert English text into:
- **Hindi (`hi`)**
- **French (`fr`)**
- **Spanish (`es`)**
- **Tamil (`ta`)**
- **Telugu (`te`)**
- **English (`en`)**  

Powered by **googletrans**.

---

### 🗣️ 4. Multi-Language & Multi-Voice TTS
Using **Edge-TTS (Microsoft Neural Voices)**:
- 140+ voices  
- High-quality natural speech  
- Multiple accents & genders  
- Saves audio as MP3  

---

### 💾 5. Audio History Storage
All generated audio files are saved inside:

## 🎵 Generated Audio

All generated MP3 files are automatically stored inside the:


The app displays a **History Table** showing:

- **File Name**
- **Audio Duration**
- **Created Date**
- **Playback**
- **Download Button**

This helps users easily access previously generated audiobooks.

## 🎨 Modern UI

The application includes a clean, modern interface built with Streamlit:

- Sidebar with **About** section  
- Two-column layout for better content flow  
- Neatly styled expandable sections  
- Smooth user experience for rewriting, translating, and generating audio  
- Automatic history table with pagination  

## 🧩 Folder Structure
```
AudioBook-Generator/
│
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md # Project documentation
│
├── generated_audio/ # Saved MP3 files
│ └── (audio files)
│
├── modules/ # Modular backend components
│ ├── tts_engine.py # Edge-TTS engine
│ ├── translator.py # Translation using googletrans
│ ├── llm_enrichment.py # Gemini + local rewrite engine
│
└── .env # API keys and environment variables
```

## 🔧 Installation

### 1️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


---
```
## 🔑 Environment Variables (Code Block)

```markdown
## 🔑 Environment Variables

Create a `.env` file in the project root:
```
GEMINI_API_KEY=YOUR_API_KEY_HERE
FFMPEG_PATH=C:\ffmpeg\bin\ffmpeg.exe



## ▶️ Running the App

```bash
streamlit run app.py
```

## 👩‍💻 Author

**Nainsi Verma**  
AI & Full-Stack Developer  
Building intelligent tools for productivity and accessibility.
