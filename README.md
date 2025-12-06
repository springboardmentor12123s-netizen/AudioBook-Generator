# 🎧 **AI AudioBook Generator**

Convert PDF, DOCX, and TXT files into high-quality audiobooks using **Gemini AI** and **Text-to-Speech** engines.

---

## 🚀 **Overview**

The **AI AudioBook Generator** is a Streamlit-based application that:

* Extracts text from uploaded PDF, DOCX, or TXT files
* Cleans & rewrites the content using **Google Gemini AI**
* Converts the enhanced text into audio (WAV/MP3)
* Allows users to **play and download** the generated audiobook
* Offers fallback offline TTS support when online TTS fails

This project enhances accessibility for students, researchers, and visually challenged readers.

---

## ⭐ **Key Features**

### 🔍 **1. Text Extraction**

Supports:

* PDF (via `pdfplumber`)
* DOCX (via `python-docx`)
* TXT files
  Cleans unwanted symbols, formatting, line breaks.

### 🤖 **2. Gemini AI Text Rewriting**

* Enhances clarity
* Fixes grammar
* Removes unwanted characters
* Makes narration-friendly text

### 🔊 **3. Text-to-Speech Conversion**

Two-layer TTS system:

* **Primary:** gTTS (online, fast, natural)
* **Fallback:** pyttsx3 (offline)

### 🖥️ **4. User-Friendly Streamlit UI**

* Upload file
* Preview extracted & enriched text
* Generate audiobook
* Play or download audio

---

## 🏗️ **Project Structure**

```
AudioBook-Generator/
│── app_streamlit_final.py
│── README.md
│── requirements.txt
│── pymod/
│   ├── text_extraction.py
│   ├── llm.py
│   ├── text2spe.py
│   ├── utils.py
│── output/
│── assets/
```

---

## 🔧 **Installation & Setup**

### **1️⃣ Clone Repository**

```bash
git clone https://github.com/your-repo-link/AudioBook-Generator.git
cd AudioBook-Generator
```

### **2️⃣ Create Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate  
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Set Gemini API Key**

Either export in terminal:

```bash
setx GEMINI_API_KEY "your_api_key_here"
```

Or paste inside the Streamlit app sidebar.

---

## ▶️ **Running the Application**

Start Streamlit:

```bash
streamlit run app_streamlit_final.py
```

Access in browser:

```
http://localhost:8501
```

---

## 🧪 **Testing**

### Things to test:

* PDF extraction
* DOCX extraction
* Long text cleaning
* Gemini rewrite quality
* Audio generation speed
* Offline TTS fallback
* Validation for empty/invalid files

Sample test:

```bash
python test_tts_batch.py
```

---

## 📦 **Deployment**

The app can be deployed using:

* **Streamlit Cloud**
* **Render**
* **Heroku**
* **Google Cloud Run**

Recommended steps:

1. Upload code to public GitHub repo
2. Configure Gemini API in deployment platform
3. Install dependencies
4. Run Streamlit server

---

## 🔮 **Future Enhancements**

* Multi-language audiobook generation
* Custom voice options
* OCR support for scanned PDFs
* Export rewritten text as PDF
* Cloud storage for user history
* Sentence-level natural prosody

---

## ❤️ **Contributors**

* **Achana Prashanth** – Developer
* Mentor & Project Guide

---

## 📜 **License**

This project is open-source under the MIT License.

