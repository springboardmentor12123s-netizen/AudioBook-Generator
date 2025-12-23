# 🎧 AI Audiobook Generator – Project

This project converts documents into clean text and prepares them for audiobook-style output.

---

## 🚀 Features Implemented

✔ Upload files: **PDF / DOCX / TXT**  
✔ Extract and display clean text from documents  
✔ Organized Streamlit UI for easy use  
✔ use an LLM to rewrite the extracted text into audiobook-style narration and LLM requires organization API key for activation


---

## 🧠 Future Enhancements (Planned)

🔹 Add LLM rewrite feature for audiobook-friendly narration  
🔹 Add Text-to-Speech (TTS) using an online service API  
🔹 Add Download button for generated audio files  

> Audio generation using gTTS is disabled on this laptop due to unstable network issues.  
> But the code already supports connecting any TTS API in the future.

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Frontend UI | Streamlit |
| Text Extraction | `pdfplumber`, `docx` |
| Code Language | Python |
| Version Control | Git + GitHub |

---

## ▶️ How to Run

### 1️⃣ Create Virtual Environment
```sh
python -m venv venv
