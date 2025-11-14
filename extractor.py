import pdfplumber
from docx import Document

def extract_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_from_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_from_txt(file):
    return file.read().decode("utf-8")

def extract_text(file, file_type):
    if file_type == "pdf":
        return extract_from_pdf(file)
    elif file_type == "docx":
        return extract_from_docx(file)
    elif file_type == "txt":
        return extract_from_txt(file)
    else:
        return "Unsupported file format"