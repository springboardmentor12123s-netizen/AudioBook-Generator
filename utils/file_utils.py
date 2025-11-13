import io
from typing import Tuple, Dict
from PyPDF2 import PdfReader
from docx import Document

ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]

def extract_text_from_file(filename: str, data: bytes) -> Tuple[str, Dict]:
    """
    Detects file type from filename and extracts plain text.
    Returns (text, metadata dict).
    """
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    meta = {"filename": filename, "extension": ext}

    if ext == "pdf":
        text = _extract_text_from_pdf(data, meta)
    elif ext == "docx":
        text = _extract_text_from_docx(data, meta)
    elif ext == "txt":
        text = _extract_text_from_txt(data, meta)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported: {ALLOWED_EXTENSIONS}")

    return text, meta


def _extract_text_from_pdf(data: bytes, meta: dict) -> str:
    buffer = io.BytesIO(data)
    reader = PdfReader(buffer)
    n_pages = len(reader.pages)
    meta.update({"pages": n_pages})
    texts = []

    for i, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        texts.append(f"\n\n--- Page {i+1} / {n_pages} ---\n\n")
        texts.append(page_text)

    return "".join(texts).strip()


def _extract_text_from_docx(data: bytes, meta: dict) -> str:
    buffer = io.BytesIO(data)
    doc = Document(buffer)
    paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip() != ""]
    meta.update({"paragraphs": len(paragraphs)})
    return "\n\n".join(paragraphs).strip()


def _extract_text_from_txt(data: bytes, meta: dict) -> str:
    # try utf-8 then fallback
    for enc in ("utf-8", "latin-1", "utf-16"):
        try:
            txt = data.decode(enc)
            meta.update({"encoding": enc})
            return txt
        except Exception:
            continue
    raise UnicodeDecodeError("Unable to decode text file with common encodings.")
    """Simple TXT extraction."""
