# text_extraction.py

import PyPDF2
import pdfplumber
from docx import Document

def extract_text_from_pdf(path):
    text = ""
    try:
        with open(path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
    except:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    return text.strip()

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs]).strip()

def extract_text_from_txt(path):
    return open(path, "r", encoding="utf-8", errors="ignore").read().strip()

def extract_text(path):
    ext = path.split(".")[-1].lower()
    if ext == "pdf": return extract_text_from_pdf(path)
    if ext == "docx": return extract_text_from_docx(path)
    if ext == "txt": return extract_text_from_txt(path)
    raise ValueError("Unsupported file format")
