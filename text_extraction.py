import PyPDF2
import pdfplumber
from docx import Document
import os

def extract_text_from_pdf(file_path):
    """
    Extract text from PDF using PyPDF2 first, and fallback to pdfplumber if PyPDF2 fails.
    """
    text = ""
    try:
        # Method 1: PyPDF2
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
    except Exception as e:
        print("PyPDF2 failed, trying pdfplumber...", e)
        # Method 2: pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    return text.strip()


def extract_text_from_docx(file_path):
    """
    Extract text from DOCX files using python-docx.
    """
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def extract_text_from_txt(file_path):
    """
    Extract text from plain TXT files.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return text.strip()


def extract_text(file_path):
    """
    Auto-detect file type and extract text accordingly.
    """
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif extension == ".docx":
        return extract_text_from_docx(file_path)
    elif extension == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")
