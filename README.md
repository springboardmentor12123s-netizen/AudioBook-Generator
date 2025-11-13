# AI Audiobook Generator — Week 1 Starter

This starter project implements the Week 1 features:
- Upload PDF / DOCX / TXT
- Extract & show text preview

---

### 🧩 Quickstart

1. **Create and activate a virtual environment**

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate

   ##  — LLM Summarization & TTS

### Options
- **OpenAI**: Set `OPENAI_API_KEY` environment variable or paste your key in the sidebar. Requires `openai` package.
- **Local Transformers**: Install `transformers` and `torch` to enable local summarizer.

### TTS options
- **gTTS** (online): produces MP3 files, requires internet.
- **pyttsx3** (offline): produces WAV files.

### Install (recommended minimal)
pip install -r requirements.txt

### Run
streamlit run app.py

