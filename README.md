# AudioBook Generator

A web application that converts documents (PDF, DOCX, TXT) into high-quality audiobooks using AI-powered text enhancement and text-to-speech.

## Features

- **Multi-format Support** - Upload PDF, DOCX, or TXT files
- **AI Text Enhancement** - Gemini AI rewrites text for natural narration
- **High-Quality Voices** - 16 premium voices via ElevenLabs
- **29 Languages** - Multi-language output support
- **Clean UI** - Modern, responsive interface with Tailwind CSS
- **Drag & Drop** - Easy file upload experience

## How It Works

```
Upload Document → Extract Text → AI Enhancement → Text-to-Speech → Download MP3
```

1. **Upload** - Drag & drop or select a document
2. **Extract** - Text is extracted from PDF/DOCX/TXT
3. **Enhance** - Gemini AI rewrites for audiobook narration
4. **Synthesize** - ElevenLabs converts to natural speech
5. **Download** - Listen in browser or download MP3

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python Flask |
| **Frontend** | HTML + Jinja2 + Tailwind CSS |
| **Text Extraction** | PyPDF2, python-docx |
| **LLM** | Google Gemini API |
| **Text-to-Speech** | ElevenLabs API |

## Project Structure

```
audio-book-generator/
├── app.py                 # Flask routes
├── config.py              # Configuration
├── modules/
│   ├── extractor.py       # Text extraction
│   ├── enricher.py        # LLM enhancement
│   └── synthesizer.py     # TTS conversion
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
├── uploads/               # Temp uploads (gitignored)
├── outputs/               # Generated audio (gitignored)
├── requirements.txt
└── .env                   # API keys (gitignored)
```

## Quick Start

### 1. Clone & Setup

```bash
cd audio-book-generator
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

**Get API Keys:**
- Gemini: https://makersuite.google.com/app/apikey
- ElevenLabs: https://elevenlabs.io/app/settings/api-keys

### 4. Run

```bash
python app.py
```

Open http://localhost:5000

## Available Voices

| Voice | Description |
|-------|-------------|
| Sarah | Soft, young American female |
| Adam | Deep, middle-aged American male |
| Rachel | Calm, young American female |
| Josh | Deep, young American male |
| Elli | Emotional, young American female |
| Antoni | Well-rounded American male |
| Charlotte | Swedish female |
| Alice | Confident, British female |
| Daniel | Deep, authoritative British male |
| + 7 more | Various accents and styles |

## Supported Languages

English, Spanish, French, German, Italian, Portuguese, Polish, Hindi, Japanese, Korean, Chinese, Arabic, Russian, Dutch, Turkish, Swedish, Indonesian, Filipino, Tamil, Ukrainian, Greek, Czech, Finnish, Romanian, Danish, Bulgarian, Malay, Slovak, Croatian

## API Limits

| Service | Free Tier |
|---------|-----------|
| Gemini | 60 requests/min |
| ElevenLabs | 10,000 characters/month |

## Architecture

```
┌─────────────────────────┐
│   User (Flask Web UI)   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│      File Upload        │
│   (PDF, DOCX, TXT)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    Text Extraction      │
│  (PyPDF2, python-docx)  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   LLM Enhancement       │
│    (Gemini API)         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Text-to-Speech        │
│   (ElevenLabs API)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    Download MP3         │
└─────────────────────────┘
```