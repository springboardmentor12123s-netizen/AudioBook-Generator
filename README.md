

# 🎧 AudioBook Generator

A professional **AudioBook Generator** built using Python and Streamlit that converts **PDF, DOCX, and TXT files** into high-quality audio. The project also supports **text summarization** and **speech-to-text utilities**, making it a complete academic and practical solution.

This README provides **step-by-step guidance** to set up, run, and understand the project.

---

## 📌 Project Overview

The AudioBook Generator allows users to:

* Upload **PDF, DOCX, or TXT** files
* Extract readable text from documents
* Convert **any text (documents, poems, stories)** into **audio speech (Text-to-Speech)**
* Upload **audio files such as songs or poems**
* **Extract lyrics or spoken text from songs, poems, or audio files (Speech-to-Text)**
* Display the extracted **lyrics/text** to the user
* (Optional) Summarize the extracted or uploaded text
* Play or download the generated audiobook

This project is suitable for:

* Academic mini-projects
* Assistive technology for visually impaired users
* Converting poems and stories into audio
* Extracting lyrics from songs for text analysis or reading

---

## 🛠️ Tech Stack

| Category                      | Technology                         |
| ----------------------------- | ---------------------------------- |
| Frontend                      | Streamlit                          |
| Backend                       | Python                             |
| Text-to-Speech                | gTTS                               |
| PDF Processing                | PyMuPDF (fitz)                     |
| DOCX Processing               | python-docx                        |
| Summarization                 | Sumy + NLTK                        |
| Speech Recognition (Optional) | Vosk                               |
| Environment                   | Python Virtual Environment (.venv) |

---

## 📂 Project Structure

```text
AudioBook-Generator/
│
├── app.py                     # Main Streamlit application
│
├── services/
│   └── audio_services.py      # Text-to-speech logic
│
├── utils/
│   ├── file_utils.py          # File upload & text extraction
│   ├── summarizer.py          # Text summarization logic
│   └── lyrics_extractor.py    # Speech-to-text utilities (Vosk)
│
├── models/
│   └── vosk-model/            # Vosk speech recognition model
│
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .venv/                     # Virtual environment
```

---

## ✅ Prerequisites

Ensure the following are installed:

* **Python 3.9 or higher**
* **pip** (Python package manager)
* **Git**

Check versions:

```bash
python --version
pip --version
git --version
```

---

## ⚙️ Step-by-Step Setup Guide:

### 1. Create and Activate Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

---

### 2. Install Required Dependencies

Create / verify `requirements.txt`:

```text
streamlit
gTTS
vosk
PyMuPDF
python-docx
sumy
nltk
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Download NLTK Resources (Required for Summarization)

```bash
python
```

```python
import nltk
nltk.download('punkt')
exit()
```

---

### 4. Download Vosk Speech Model (Optional Feature)

Download a model such as:

* `vosk-model-small-en-us-0.15`

Extract it into:

```text
models/vosk-model-small-en-us-0.15/
```

Ensure your code loads it correctly:

```python
model = Model("models/vosk-model-small-en-us-0.15")
```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at:

```
http://localhost:8501
```

---

## 🧪 Supported File Formats

### 📄 Document Inputs

* ✅ PDF (.pdf)
* ✅ Word (.docx)
* ✅ Text (.txt)

### 🎵 Audio Inputs

* ✅ WAV audio files (songs, poems, or spoken audio)

### 📜 Extracted Output

* ✅ Lyrics or spoken text extracted from songs and poems

### 🔊 Audio Outputs

* ✅ MP3 audio files generated from text (documents, poems, or extracted lyrics))

* ✅ PDF (.pdf)

* ✅ Word (.docx)

* ✅ Text (.txt)

---

## 🔐 Git Workflow (Important)

### Add and Commit Changes

```bash
git add .
git commit -m 
```

### Push ONLY to Your Branch

```bash
git push origin Branch_name
```

🚫 **Never push to `main`**

---

## 🚨 Common Errors & Fixes

| Error               | Solution                          |
| ------------------- | --------------------------------- |
| ModuleNotFoundError | Install missing library using pip |
| fitz not found      | Install PyMuPDF                   |
| docx not found      | Install python-docx               |
| NLTK punkt error    | Download nltk punkt               |
| Vosk model error    | Check model path                  |

---

## 🎯 Future Enhancements

* Add multilingual support
* Improve UI/UX
* Cloud deployment
* Advanced neural TTS models

---

## 👩‍💻 Author

**Ayushi Singh**
Third Year Student
AudioBook Generator Project

---

## ⭐ Acknowledgements

* Streamlit Team
* Open-source Python Community
* Mentor Guidance

---

✨ *This project follows professional Git and Python development practices.*

