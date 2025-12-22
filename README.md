

 🎧 AI AudioBook Generator
1. Project Overview

The **AI AudioBook Generator** is a smart web application that converts static documents (PDF, DOCX, TXT) into engaging, high-quality audiobooks. Unlike standard text-to-speech tools, this project uses **Generative AI** to rewrite and "polish" the text into a conversational script before converting it to audio. It also features a robust **Translation Engine**, allowing users to listen to their documents in their native languages (e.g., Telugu, Hindi, Spanish).

**Problem Solved:** Reading long, dry technical documents or PDFs can be exhausting. This tool makes knowledge accessible by turning reading material into an easy-to-listen audio experience.

 2. Key Features

* **📂 Multi-Format Support:** Instantly extracts text from **PDFs**, **Word Documents**, and **Text files**.
* **✨ AI Script Enrichment:** Uses **Large Language Models (LLMs)** to rewrite dry content into an engaging, story-like script.
* **🌍 Smart Translation:** Reliably translates content from English to **Telugu**, **Hindi**, **Tamil**, **Spanish**, and **French**.
* **🗣️ Hybrid Audio Engine:**
* **Online Mode (gTTS):** High-quality, natural-sounding voices for multiple languages.
* **Offline Mode (System Voice):** Fast, privacy-focused audio generation that works without the internet.


* **💻 Interactive UI:** A clean, modern web interface built with **Streamlit**.

3. Technology Stack

* **Frontend:** Streamlit (Python Web Framework)
* **Language Models (LLM):** OpenRouter API (Accessing models like Mistral 7B, Google Gemini, Microsoft Phi-3)
* **Translation:** `deep-translator` (Google Translate API wrapper)
* **Audio Processing:**
* `gTTS` (Google Text-to-Speech)
* `pyttsx3` (Offline System TTS)


* **Data Handling:** `PyPDF2`, `python-docx`

 4. Installation & Setup

**Prerequisites:**

* Python 3.8 or higher installed.
* An API Key from OpenRouter

**Step 1: Clone/Download the Project**
Create a folder named `AI_AudioBook` and place all project files inside it.

**Step 2: Create Virtual Environment**
Open your terminal in the project folder and run:

```bash
# Create the environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\Activate

```

**Step 3: Install Dependencies**

```bash
pip install -r requirements.txt

```

**Step 4: Configure API Key**
Create a file named `.env` in the folder and add your key:

```text
OPENROUTER_API_KEY="sk-or-v1-YOUR_KEY_HERE"

```

**Step 5: Run the Application**

```bash
streamlit run app.py

```

 5. Project Structure

Here is how the code is organized:

```text
AI_AudioBook/
├── app.py                # Main User Interface (Frontend)
├── utils.py              # Helper functions (PDF reading, Translation, Audio generation)
├── llm.py                # AI Logic (Connects to OpenRouter for rewriting)
├── .env                  # Stores your secret API Key
├── requirements.txt      # List of all required Python libraries
└── README.md             # This documentation file

```

6. Usage Guide

1. **Upload:** Drag and drop your PDF or Word file into the sidebar.
2. **Select Engine:** Choose **gTTS** for foreign languages or **System Voice** for fast English audio.
3. **Select Language:** If using gTTS, pick your target language (e.g., Telugu).
4. **Generate:** Click the "Generate Audiobook" button.
5. **Listen:** The app will display the original text, the rewritten script, and an audio player. You can download the MP3 file to your device.

 7. Future Enhancements

* **Voice Cloning:** Allow users to upload a sample voice to narrate the book.
* **Long-Form Support:** Add "chunking" to handle entire novels (300+ pages) automatically.
* **OCR Support:** Add ability to read text from scanned images/screenshots.
* **Mobile App:** Convert the interface into a dedicated mobile application.

 8. Contributors

* **Developer:** Jami Sai Dinesh
* **Tech Stack:** Python & Streamlit Community
