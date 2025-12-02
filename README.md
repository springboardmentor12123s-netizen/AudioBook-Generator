# 🎧 AI Audiobook Generator

The **AI Audiobook Generator** is a Streamlit-based web application that converts your documents (PDF, DOCX, TXT) into high-quality audiobooks. It extracts text, enhances it using Google Gemini, and converts the narration into MP3 audio using gTTS.

---

## 🚀 Features

- Upload PDF, DOCX, or TXT files  
- Extract clean text from documents  
- Enhance text using Google Gemini for audiobook-style narration  
- Convert enhanced text to MP3 audio  
- Preview extracted & enhanced text  
- Built-in audio player + download button  
- Simple & modular codebase  

---

## 🧠 Technology Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Text Extraction | PyPDF2, python-docx |
| AI Enhancement | Google Gemini API |
| Text-to-Speech | gTTS |
| Language | Python 3.x |

---

## 📁 Project Structure

```

.
├── app.py               # Main Streamlit interface
├── text_extractor.py    # Extracts text from PDF, DOCX, TXT files
├── llm_enhancer.py      # AI-based text enhancement using Gemini
├── tts_generator.py     # Generates audio using gTTS
│
├── test_sample.txt      # Sample text for testing
├── requirements.txt     # All Python dependencies
└── README.md            # Project documentation

```

---

## 🔐 Environment Setup

This application requires a Google Gemini API key.

Create a `.env` file:

```

GEMINI_API_KEY=your_api_key_here

```

⚠️ Do NOT upload `.env` to GitHub.

---

## 🛠 Installation & Running Locally

### 1. Clone the repository
```

git clone [https://github.com/yourusername/AI-Audiobook-Generator.git](https://github.com/yourusername/AI-Audiobook-Generator.git)
cd AI-Audiobook-Generator

```

### 2. Create a virtual environment

#### Windows
```

python -m venv venv
venv\Scripts\activate

```

#### macOS/Linux
```

python3 -m venv venv
source venv/bin/activate

```

### 3. Install dependencies
```

pip install -r requirements.txt

```

### 4. Set up your Gemini API key
Create a `.env` file:

```

GEMINI_API_KEY=your_api_key_here

```

### 5. Run the application
```

streamlit run app.py

```

### 6. Open in browser
Go to:

```

[http://localhost:8501]

```

Upload your documents → Generate audiobook → Download your MP3.

---

## 🧪 Workflow Explained

1. User uploads a file (PDF, DOCX, or TXT)  
2. `text_extractor.py` extracts clean text  
3. `llm_enhancer.py` rewrites text using Google Gemini  
4. `tts_generator.py` converts enhanced text to MP3  
5. User previews and downloads the audio  

---
