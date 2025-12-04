📘 AI Audiobook Generator (Gemini + gTTS)

Convert PDF / DOCX / TXT into complete audiobook chapters automatically.

This system extracts text from documents, splits it into chapters, rewrites each chapter using Google Gemini in audiobook-style narration, and generates MP3 audio files for:

🔊 Original content narration
🎙 Rephrased audiobook-style narration

Users can preview text versions and download audio per chapter.

🚀 Features
Feature	Status
Upload PDF / DOCX / TXT	✔
Automatic chapter detection	✔
Google Gemini rephrasing	✔
Audio narration using gTTS	✔
Indian / US / UK / Australian voice accents	✔
Listen to & download original audio	✔
Listen to & download rephrased audio	✔
Multiple file upload support	✔
🧠 How it works (pipeline)
Upload document → Extract Text → Split into Chapters
     ↓
Actual Chapter Text → Original Audio (Speech)
     ↓
Gemini Rephrasing → Rephrased Chapter Text → Rephrased Audio


User receives two versions of audio for every chapter:

Actual/original voice narration

Rephrased audiobook-style narration

📂 Project Structure
AI_AudioBook_Generator/
│ app.py
│ requirements.txt
│ .env   (not included in repo)
│ .gitignore
│
├─ utils/
│   extract_text.py
│   chapters.py
│   enrich_text.py
│   tts.py
│
└─ outputs/
    └─ audio/   (generated MP3 files)

🔧 Requirements

Install all dependencies:

pip install -r requirements.txt


If running manually:

pip install streamlit PyPDF2 python-docx gTTS google-generativeai python-dotenv

🔑 Environment Setup

Create a .env file in project root:

GEMINI_API_KEY=your_api_key_here


⚠ Do NOT commit .env to GitHub.

▶️ Run the application

In terminal inside the project folder:

streamlit run app.py


App will open in the browser (default: http://localhost:8501
)

📸 UI Output Example

For every chapter you get:

Output	Format
Actual content text	text preview + download
Rephrased content text	text preview + download
Original audio	MP3 + player + download
Rephrased audio	MP3 + player + download
🔐 .gitignore (recommended)
.env
outputs/
*.mp3
.venv/
__pycache__/

🛠 Future Enhancements (optional)

OpenAI TTS for human-like narrator voices

Export full audiobook in a single MP3

Add background music & sound effects

Deploy on Streamlit Cloud / HuggingFace Space

Generate EPUB + MP3 audiobook bundle

🤝 Contributing

Pull Requests are welcome!
If contributing major changes, please open an issue first to discuss improvements.

📜 License

This project can be licensed under MIT License (optional — add LICENSE file if you want).

💙 Credits

Developed with ❤️ using:

Google Gemini

Streamlit

gTTS

Python
