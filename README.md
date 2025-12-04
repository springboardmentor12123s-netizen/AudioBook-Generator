# Grammar-Correcting Multi-Language AudioBook Generator

**Author:** Jeeval Shah  
**Version:** 1.0  
**Target Audience:** Individuals with visual impairments, auditory learners, and users seeking productivity tools for document consumption.

---

## 1. Overview
The **AudioBook Generator** is a sophisticated Streamlit-based web application that transforms static documents (PDF, DOCX, TXT) into high-quality, listenable audiobooks. 

Unlike standard TTS converters, this tool leverages **Google's Gemini AI** to first correct grammar and enhance the readability of the text. It also offers AI-powered translation into 12 major languages before generating audio, ensuring a smooth and natural listening experience across language barriers.

---

## 2. Features
* **Multi-Format Ingestion:** Seamlessly processes `.pdf`, `.docx`, and `.txt` files.
* **AI-Powered Grammar Correction:** Uses Google Gemini (Generative AI) to fix grammatical errors and smooth out text flow before conversion.
* **Multi-Language Support:** Translates content into 12 languages (including Hindi, Spanish, French, Chinese, etc.) prior to audio generation.
* **Smart Number Processing:** Automatically converts numerical digits (e.g., "1995") into words (e.g., "nineteen ninety-five") for natural speech.
* **Dual Audio Output:** Generates and allows downloads for both the **original (corrected)** audio and the **translated** audio.
* **Robust Error Handling:** Includes logic for file extraction errors, API limits, and text truncation.

---

## 3. Technology Stack
| Component | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Frontend/UI** | Streamlit | Interactive web interface for file upload and controls. |
| **LLM / AI** | Google Gemini API | Grammar correction and multi-language translation. |
| **Text-to-Speech** | gTTS (Google TTS) | Converting processed text into MP3 audio. |
| **Text Processing** | PyPDF2, python-docx, num2words | Extracting text from files and normalizing numbers. |
| **Backend** | Python 3.x | Core application logic. |
| **Configuration** | python-dotenv | Secure management of API keys. |

---

## 4. Requirements Document

### 4.1 Functional Requirements
1.  **Document Upload:** Users must be able to upload PDF, Word, or Text files.
2.  **Text Extraction:** The system must parse binary files to extract readable text strings.
3.  **Grammar Sanitization:** The system must send extracted text to the Gemini LLM to correct syntax and grammar errors.
4.  **Translation:** The system must allow users to select a target language and translate the corrected text using LLM.
5.  **Audio Synthesis:** The system must generate `.mp3` files for both the corrected English text and the translated text.

### 4.2 Non-Functional Requirements
* **Scalability:** Text exceeding 30,000 characters must be truncated to prevent API token overflow.
* **Security:** API keys must be loaded via environment variables (`.env`) and not hardcoded.
* **Usability:** The UI must provide visual feedback (spinners) during the extraction and generation processes.

---

## 5. Execution Plan (Timeline vs. Implementation)

| Phase | Timeline | Objective | Implementation Status |
| :--- | :--- | :--- | :--- |
| **1** | Weeks 1-2 | **Setup & Extraction** | **Completed:** Environment set up, `extract_text()` function implemented for all file types. |
| **2** | Weeks 3-4 | **AI Integration** | **Completed:** `google.generativeai` configured. `grammar_correction` and `translate_text` functions operational. |
| **3** | Weeks 5-6 | **Audio Synthesis** | **Completed:** `gTTS` integrated. Added `num2words` for better numeric pronunciation. |
| **4** | Weeks 7-8 | **UI & Optimization** | **Ongoing:** Streamlit UI built with progress spinners, audio players, and download buttons. |

---

## 6. Analysis of Requirements & Development

This section details how specific technical challenges were addressed in the code.

### 6.1 Logic: Text Extraction Strategy
* **Challenge:** Different file types store text differently.
* **Solution:** A routing function `extract_text(file)` checks the file extension.
    * `.pdf`: Uses `PdfReader` to iterate through pages.
    * `.docx`: Uses `Document` to iterate through paragraphs.
    * `.txt`: Uses standard UTF-8 decoding.

### 6.2 Logic: Enhancing Audio Quality
* **Challenge:** Raw text often contains abbreviations or numbers (e.g., "10kg") that TTS engines read awkwardly.

* **Solution:**
    1.  **Grammar Pass:** Text is sent to Gemini with the prompt: *"Correct grammatical errors... Return only the improved text."*
    2.  **Numeric Pass:** Regex finds digits and `num2words` converts them to string representations before the TTS engine receives them.

### 6.3 Logic: Multi-Language Architecture
* **Challenge:** `gTTS` requires specific language codes (ISO 639-1).

* **Solution:** A dictionary `SUPPORTED_LANGUAGES` maps user-friendly names (e.g., "Chinese (Simplified)") to codes (`zh`), ensuring the TTS engine receives the correct instruction.

---

## 7. Installation & Setup

Follow these steps to run the application locally.

### Step 1: Clone the repository (Branch: jeeval_shah)
```bash
git clone -b jeeval_shah [https://github.com/springboardmentor12123s-netizen/AudioBook-Generator.git](https://github.com/springboardmentor12123s-netizen/AudioBook-Generator.git)
cd AudioBook-Generator
```

### Step 2: Create a virtual environment

```bash
conda create -n 'audiobook' python=3.10
conda activate audiobook

# OR for standard python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys
Create a file named .env in the root directory and add your Google Gemini API key:

```bash
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Run the App
```bash
streamlit run app.py
```

## 8. Usage Guide
    1. Upload: Drag and drop your file into the uploader.
    2. Verify: Check the "Original Extracted Text" box to ensure the file was read correctly.
    3. Select Language: Choose your desired output language from the dropdown.
    4. Generate: Click "Process and Generate Audio".
       Note: This process may take 30-60 seconds depending on text length.
    6. Download: Use the audio players to listen immediately, or click the "Download" buttons to save the .mp3 files.