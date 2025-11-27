# extract_text.py
import io
import pdfplumber
from docx import Document

def extract_from_pdf(file_stream):
    # file_stream: a BytesIO or file-like object
    text_parts = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n\n".join(text_parts).strip()

def extract_from_docx(file_stream):
    # file_stream: BytesIO
    doc = Document(file_stream)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return "\n\n".join(paragraphs).strip()

def extract_from_txt(file_stream):
    file_stream.seek(0)
    raw = file_stream.read()
    if isinstance(raw, bytes):
        raw = raw.decode(errors="ignore")
    return raw.strip()

def extract_text(uploaded_file):
    """
    uploaded_file: streamlit UploadedFile (has .name and .read())
    Return extracted text string
    """
    name = uploaded_file.name.lower()
    raw = io.BytesIO(uploaded_file.read())
    if name.endswith(".pdf"):
        return extract_from_pdf(raw)
    elif name.endswith(".docx"):
        return extract_from_docx(raw)
    elif name.endswith(".txt"):
        return extract_from_txt(raw)
    else:
        raise ValueError("Unsupported file type. Supported: PDF, DOCX, TXT")