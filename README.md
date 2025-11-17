# 🎧 AI AudioBook Generator

Transform your documents into engaging audiobooks using AI-powered text enrichment and text-to-speech technology!

## 📋 Overview

AudioBook Generator is a web application that allows users to upload text documents (PDF, DOCX, TXT) and automatically converts them into high-quality audiobooks. The application leverages Large Language Models (LLMs) to rewrite extracted text in an engaging, listener-friendly audiobook style before using text-to-speech (TTS) technology to produce downloadable audio files.

## ✨ Features

- **Multi-Format Support**: Upload PDF, DOCX, and TXT files
- **AI Text Enrichment**: Use OpenAI (GPT-3.5/GPT-4) or Google Gemini to enhance text for audiobook narration
- **Multiple TTS Engines**: Choose between Google TTS (online) or pyttsx3 (offline)
- **Customizable Voice Settings**: Adjust speech rate and volume for pyttsx3
- **User-Friendly Interface**: Built with Streamlit for an intuitive experience
- **Batch Processing**: Upload and process multiple documents at once
- **Preview Options**: View extracted and enriched text before conversion
- **Instant Download**: Download your generated audiobook as MP3

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd AI-Audiobook-Generator
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\\Scripts\\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API keys** (optional, only if using LLM enrichment):
   - For OpenAI: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - For Google Gemini: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - You can enter these directly in the app's sidebar when running

### Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to the URL shown (typically `http://localhost:8501`)

3. **Upload your documents** and configure settings in the sidebar

4. **Click "Generate AudioBook"** and wait for processing

5. **Download your audiobook**!

## 📁 Project Structure

```
AI-Audiobook-Generator/
├── app.py                  # Main Streamlit application
├── extract.py              # Text extraction module
├── llm_enrichment.py       # LLM text enrichment module  
├── tts_converter.py        # Text-to-speech conversion module
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .venv/                 # Virtual environment (created locally)
```

## 🛠️ Technology Stack

### Frontend
- **Streamlit**: Interactive web interface

### Text Extraction
- **pdfplumber**: PDF text extraction
- **python-docx**: DOCX text extraction
- **Native Python**: TXT file reading

### LLM Integration
- **OpenAI API**: GPT-3.5-turbo, GPT-4
- **Google Gemini API**: Gemini-pro

### Text-to-Speech
- **gTTS**: Google Text-to-Speech (online)
- **pyttsx3**: Offline TTS engine

## 📖 Usage Guide

### Step 1: Configure Settings

In the sidebar, you can:
- Select your preferred LLM provider (or skip enrichment)
- Choose a TTS engine
- Adjust voice settings (for pyttsx3)
- Enter your API key (if using LLM enrichment)

### Step 2: Upload Documents

- Click "Browse files" to select one or more documents
- Supported formats: PDF, DOCX, TXT
- You can upload multiple files at once

### Step 3: Generate AudioBook

- Click the "🎵 Generate AudioBook" button
- The app will:
  1. Extract text from your documents
  2. Enrich the text with AI (if selected)
  3. Convert to speech
  4. Display the audio player

### Step 4: Download

- Listen to the preview
- Click "⬇️ Download AudioBook" to save the MP3 file

## ⚙️ Configuration Options

### LLM Providers

1. **OpenAI (GPT-3.5)**: Fast and cost-effective
2. **OpenAI (GPT-4)**: Higher quality, more expensive
3. **Google Gemini**: Alternative LLM option
4. **Skip Enrichment**: Use original text without AI enhancement

### TTS Engines

1. **gTTS (Google)**: 
   - Pros: High-quality, natural-sounding voices
   - Cons: Requires internet connection

2. **pyttsx3 (Offline)**:
   - Pros: Works offline, customizable
   - Cons: Less natural sounding

## 🔧 Development

### Module Breakdown

#### `extract.py`
Handles text extraction from different file formats:
- `extract_text_from_pdf()`: Extracts text from PDF files
- `extract_text_from_docx()`: Extracts text from DOCX files
- `extract_text_from_txt()`: Reads TXT files

#### `llm_enrichment.py`
Enriches text using LLMs:
- `enrich_text_with_llm()`: Rewrites text for audiobook narration
- Handles chunking for long texts
- Supports multiple LLM providers

#### `tts_converter.py`
Converts text to speech:
- `convert_to_speech()`: Generates audio files
- Supports multiple TTS engines
- Customizable voice parameters

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors**:
   ```bash
   pip install -r requirements.txt
   ```

2. **API key errors**:
   - Ensure your API key is valid
   - Check that you have available credits/quota

3. **pyttsx3 not working on Linux**:
   ```bash
   sudo apt-get install espeak
   ```

4. **PDF extraction issues**:
   - Try using a different PDF library or convert to DOCX/TXT first

## 📝 Week-wise Implementation

### Weeks 1-2: Foundation
- ✅ Set up environment and dependencies
- ✅ Implement file upload and text extraction
- ✅ Support for PDF, DOCX, and TXT formats

### Weeks 3-4: AI Integration
- ✅ Integrate LLM for text enrichment
- ✅ Build API connection for OpenAI and Gemini
- ✅ Implement text chunking for long documents

### Weeks 5-6: TTS Implementation
- ✅ Integrate gTTS and pyttsx3
- ✅ Add voice customization options
- ✅ Implement error handling

### Weeks 7-8: Finalization
- ✅ Complete Streamlit UI/UX
- ✅ Add progress tracking and previews
- ✅ Write comprehensive documentation
- ✅ Testing and optimization

## 🎯 Future Enhancements

- [ ] Support for more document formats (EPUB, HTML)
- [ ] Multi-language support
- [ ] Voice cloning options
- [ ] Background music and sound effects
- [ ] Chapter detection and splitting
- [ ] Cloud storage integration
- [ ] User authentication and history

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as part of a software engineering project.

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- OpenAI and Google for their powerful LLM APIs
- The open-source community for TTS libraries

---

**Made with ❤️ by Vivek**