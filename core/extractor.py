from pathlib import Path
from typing import List

from PyPDF2 import PdfReader
import pdfplumber
import docx


def _read_pdf(uploaded_file) -> str:
    """
    Try to read text from a PDF using PyPDF2 first,
    and pdfplumber as a fallback.
    """
    # First try PyPDF2
    try:
        reader = PdfReader(uploaded_file)
        pages_text = []
        for page in reader.pages:
            txt = page.extract_text()
            if txt:
                pages_text.append(txt)
        text = "\n".join(pages_text).strip()
        if text:
            return text
    except Exception:
        pass

    # Fallback to pdfplumber
    try:
        uploaded_file.seek(0)
        with pdfplumber.open(uploaded_file) as pdf:
            pages_text = []
            for page in pdf.pages:
                txt = page.extract_text()
                if txt:
                    pages_text.append(txt)
        return "\n".join(pages_text).strip()
    except Exception:
        return ""


def _read_docx(uploaded_file) -> str:
    doc = docx.Document(uploaded_file)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def _read_txt(uploaded_file) -> str:
    data = uploaded_file.read()
    if isinstance(data, bytes):
        return data.decode("utf-8", errors="ignore").strip()
    return str(data).strip()


def extract_texts(uploaded_files: List) -> str:
    """
    uploaded_files: list of Streamlit UploadedFile objects.
    Returns ONE big string with headings per file,
    which app.py shows in a single text area.
    """
    chunks = []

    for f in uploaded_files:
        name = f.name
        suffix = Path(name).suffix.lower()

        if suffix == ".pdf":
            text = _read_pdf(f)
        elif suffix == ".docx":
            text = _read_docx(f)
        elif suffix == ".txt":
            text = _read_txt(f)
        else:
            text = ""

        if not text:
            text = "[No text could be extracted from this file]"

        # nice heading per file
        chunk = f"===== {name} =====\n{text}"
        chunks.append(chunk)

        # reset file pointer in case Streamlit reuses it
        f.seek(0)

    return "\n\n\n".join(chunks)
