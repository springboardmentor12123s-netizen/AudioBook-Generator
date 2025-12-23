# 🎧 Multilingual AI Audiobook Generator

🔗 **Live Demo:**  
👉 https://rajpal18-ai-based-auido-generator-app-h96ltx.streamlit.app/

The **Multilingual AI Audiobook Generator** allows users to upload **PDF / DOCX / TXT** documents and automatically convert them into **audiobook-style MP3 narration**.

The system can:
- Detect the original language of the document
- Generate audio in the original language
- Translate and rewrite content in an audiobook-friendly style
- Generate audio in a selected target language

---

## 🚀 Key Features

- Upload **PDF / DOCX / TXT** files
- Automatic language detection
- Chapter-based text processing
- Generate two types of audio:
  - Original-language narration
  - Translated & rephrased audiobook narration
- Supports **7 languages**:
  - English
  - Hindi
  - Marathi
  - Tamil
  - Telugu
  - Bengali
  - Gujarati
- Streamlit-based clean user interface

---

## 🛠 Technology Stack

| Component | Technology |
|--------|------------|
| UI | Streamlit |
| Text Extraction | PyPDF2, python-docx |
| AI Model | Google Gemini |
| Text-to-Speech | gTTS |
| Language Translation & Rephrasing | Gemini NLP |
| Environment Management | python-dotenv |

---

## 📂 Project Structure

```text
Multilingual_Audiobook/
│
├── app.py
├── requirements.txt
├── .env                # Not uploaded to GitHub
├── .gitignore
│
├── utils/
│   ├── extract_text.py
│   ├── chapters.py
│   ├── nlp.py
│   └── tts.py
│
└── outputs/
    └── audio/          # Generated audio saved here

⚙ Installation & Setup
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Add your Gemini API key

Create .env file in project root:

GEMINI_API_KEY=your_api_key_here

3️⃣ Run the application
streamlit run app.py

▶ How It Works

Upload one or more documents

System extracts text and splits into chapters

For each chapter:

Detects original language

Optionally generates original-language audio

Translates + rephrases content into selected language

Optionally generates translated audiobook audio

Audio can be played in the browser or downloaded as MP3

📌 Functional Requirements

User should be able to upload PDF / DOCX / TXT

System must detect document language automatically

System must allow users to select output language

Users should be able to choose:

Original audio

Translated audio

Or both

MP3 files should be downloadable

📌 Non-Functional Requirements

System should generate responses within reasonable time

User interface must be simple and easy to follow

API key must not be exposed publicly

Output should be clear and understandable narration

Project should run on any OS (Windows/Mac/Linux)

🙌 Contribution Guidelines

Pull requests are welcome.
Please open an issue first to discuss major changes.

🔒 Security Notes

⚠ Do not upload .env file to GitHub
⚠ Do not push generated .mp3 files — they are ignored via .gitignore
