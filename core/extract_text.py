import io
from typing import List
import pdfplumber
import docx


def extract_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()


def extract_from_docx(file_bytes: bytes) -> str:
    file_stream = io.BytesIO(file_bytes)
    document = docx.Document(file_stream)
    return "\n".join(p.text for p in document.paragraphs).strip()


def extract_from_txt(file_bytes: bytes) -> str:
    return file_bytes.decode(errors="ignore").strip()


def extract_text_from_files(files) -> str:
    all_text: List[str] = []
    for f in files:
        data = f.read()
        name = f.name.lower()

        if name.endswith(".pdf"):
            all_text.append(extract_from_pdf(data))
        elif name.endswith(".docx"):
            all_text.append(extract_from_docx(data))
        elif name.endswith(".txt"):
            all_text.append(extract_from_txt(data))
        else:
            all_text.append(f"[Unsupported file type: {f.name}]")

    return "\n\n".join(t for t in all_text if t).strip()
