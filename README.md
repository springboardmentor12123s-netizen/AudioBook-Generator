# 🎧 AI AudioBook Generator

Transform your documents into **high-quality audiobooks** using the power of **AI + Text-to-Speech**.  
This app extracts text from uploaded files (PDF, DOCX, TXT), rewrites it into an engaging **audiobook narration style** using **Gemini AI**, and converts it into natural-sounding speech using **Coqui TTS** — making reading effortless, fun, and accessible for everyone.

---

## 🚀 **Project Overview**

The **AI AudioBook Generator** bridges the gap between written and spoken content.  
Instead of reading long documents, users can **listen** to them as expressive, human-like audiobooks.  
It’s built for accessibility, productivity, and the joy of storytelling.

**Core Flow:**
1. 📤 Upload a document  
2. 🧠 Gemini AI rewrites text for narration  
3. 🎙 Coqui TTS converts it into speech  
4. 💾 Download or listen to your audiobook instantly  

---

## 🧩 **Features**

- 📚 Multi-format document support (PDF, DOCX, TXT)  
- 🧠 AI-powered text enhancement using Gemini LLM  
- 🎧 Natural speech generation via Coqui TTS  
- ⚙️ Offline fallback using pyttsx3  
- 🖥 Clean Streamlit web UI  
- 💾 Instant audio download (.wav / .mp3)  

---

## 🏗️ **System Architecture**

User Upload → Text Extraction → AI Enrichment → TTS Generation → Audio Download

markdown
Copy code

- **Text Extraction:** PyPDF2, pdfplumber, python-docx  
- **LLM Enrichment:** Google Gemini API  
- **Text-to-Speech:** Coqui TTS (primary) + pyttsx3 (fallback)  
- **Frontend:** Streamlit  
- **Language:** Python 3.11  

---

## ⚙️ **Installation & Setup**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Harsha-2005/AI-AudioBook-Generator.git
cd AI-AudioBook-Generator
2️⃣ Create a Virtual Environment
bash
Copy code
python -m venv env
source env/bin/activate        # macOS/Linux
env\Scripts\activate           # Windows
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Install System Dependencies
🪟 Windows
Download eSpeak NG

Extract it to C:\Program Files\eSpeak NG\

Add this path to Environment Variables → Path

Restart your terminal.

🐧 Linux / Ubuntu
bash
Copy code
sudo apt update
sudo apt install espeak-ng
🍎 macOS
bash
Copy code
brew install espeak
🔑 API Configuration
🔹 Gemini API Setup
Visit https://makersuite.google.com/app/apikey

Copy your API key.

Set it as an environment variable:

Windows PowerShell:

bash
Copy code
setx GEMINI_API_KEY "your_api_key_here"
macOS/Linux:

bash
Copy code
export GEMINI_API_KEY="your_api_key_here"
🧠 Project Structure
php
Copy code
AI-AudioBook-Generator/
│
├── app.py                    # Streamlit web interface
├── text_extraction.py        # File upload & text parsing logic
├── llm_enrichment.py         # Gemini AI text enhancement module
├── tts_generator.py          # Coqui + pyttsx3 text-to-speech engine
├── requirements.txt          # Dependency list
└── README.md                 # Project documentation
🖥️ Usage
Run the Streamlit App
bash
Copy code
streamlit run app.py
In the Web UI:
Upload your document (PDF, DOCX, or TXT)

Wait for text extraction

Click Generate Audiobook 🎙️

Listen to or download your generated audio

🧪 Example Output
Input → AI_and_Future.pdf
Output → AI_and_Future_Audiobook.wav

“Artificial Intelligence is reshaping the world around us —
from how we work to how we dream of the future.”

🧰 Tech Stack
Layer	Technology
Frontend	Streamlit
Backend	Python 3.11
AI Model	Gemini 1.5 Flash / Pro
TTS Engine	Coqui TTS + pyttsx3
Text Extraction	PyPDF2, pdfplumber, python-docx
Dependencies	google-generativeai, torch, numpy, pandas

🧩 Future Enhancements
🗣️ Multi-voice & accent customization

🌍 Multilingual support (English, Telugu, Hindi, etc.)

🎵 Background music blending

🔉 Chapter-wise audio segmentation

☁️ Cloud deployment (Hugging Face / Streamlit Cloud)

💡 Use Cases
🎓 Students converting notes and textbooks into audio

🧠 Professionals listening to reports on the go

♿ Accessibility for visually impaired users

🎙 Podcasters generating narrated content

🌐 Live Demo (Optional)
After deployment, you can host it at:

arduino
Copy code
https://ai-audiobook-generator.streamlit.app/
or on Hugging Face Spaces:

ruby
Copy code
https://huggingface.co/spaces/Harsha/AI-AudioBook-Generator
🏷️ Recommended Tags
less
Copy code
#AI #LLM #Gemini #TTS #Streamlit #Python #Audiobook #Accessibility #MachineLearning #VoiceAI #OpenSource
🧑‍💻 Author
Harsha — AI & ML Engineer in progress ⚡
Building smart, accessible tools powered by artificial intelligence.

📫 Connect:

LinkedIn

GitHub