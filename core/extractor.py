
from typing import List, Dict
from io import BytesIO
import pdfplumber
from docx import Document

def _extract_pdf(file_bytes: bytes) -> str:
    text = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text).strip()

def _extract_docx(file_bytes: bytes) -> str:
    bio = BytesIO(file_bytes)
    doc = Document(bio)
    return "\n".join([p.text for p in doc.paragraphs]).strip()

def _extract_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8", errors="ignore").strip()
    except Exception:
        return ""

def extract_texts(uploaded_files: List) -> Dict[str, str]:
    out = {}
    for f in uploaded_files:
        name = f.name
        data = f.read()
        if name.lower().endswith(".pdf"):
            out[name] = _extract_pdf(data)
        elif name.lower().endswith(".docx"):
            out[name] = _extract_docx(data)
        elif name.lower().endswith(".txt"):
            out[name] = _extract_txt(data)
        else:
            out[name] = "[Unsupported file type]"
    return out
