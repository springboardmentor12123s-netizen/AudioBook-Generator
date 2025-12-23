from pathlib import Path
from typing import List
import pdfplumber
from PyPDF2 import PdfReader
import docx


def extract_pdf(file):
    try:
        reader = PdfReader(file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if text.strip():
            return text.strip()
    except:
        pass

    try:
        file.seek(0)
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            return text.strip()
    except:
        return ""


def extract_docx(file):
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def extract_txt(file):
    data = file.read()
    return data.decode("utf-8", errors="ignore").strip()


def extract_texts(uploaded_files: List) -> str:
    combined = []
    for f in uploaded_files:
        ext = Path(f.name).suffix.lower()

        if ext == ".pdf":
            text = extract_pdf(f)
        elif ext == ".docx":
            text = extract_docx(f)
        elif ext == ".txt":
            text = extract_txt(f)
        else:
            text = ""

        if not text:
            text = "[No text extracted]"

        combined.append(f"===== {f.name} =====\n{text}\n")
        f.seek(0)

    return "\n".join(combined)
