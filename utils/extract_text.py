# utils/extract_text.py

import io
from typing import List

from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file_like: io.BytesIO) -> str:
    """
    Extract text from a PDF file-like object using PyPDF2.
    """
    reader = PdfReader(file_like)
    texts: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        texts.append(text)
    return "\n".join(texts)


def extract_text_from_docx(file_like: io.BytesIO) -> str:
    """
    Extract text from a DOCX file-like object using python-docx.
    """
    document = Document(file_like)
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def extract_text_from_txt(file_like: io.BytesIO) -> str:
    """
    Extract text from a TXT file-like object.
    """
    content = file_like.read()
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1", errors="ignore")


def extract_text_any(file_name: str, file_like: io.BytesIO) -> str:
    """
    Detect file type and extract text.
    Supports: .pdf, .docx, .txt
    """
    file_name_l = file_name.lower()
    file_like.seek(0)

    if file_name_l.endswith(".pdf"):
        return extract_text_from_pdf(file_like)
    elif file_name_l.endswith(".docx"):
        return extract_text_from_docx(file_like)
    elif file_name_l.endswith(".txt"):
        return extract_text_from_txt(file_like)
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")
