"""
Text Extraction Module
Extracts text from PDF, DOCX, and TXT files
"""

import PyPDF2
from docx import Document


def extract_from_pdf(filepath):
    """Extract text from PDF file"""
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_from_docx(filepath):
    """Extract text from DOCX file"""
    doc = Document(filepath)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()


def extract_from_txt(filepath):
    """Extract text from TXT file"""
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read().strip()


def extract_text(filepath, file_type):
    """
    Main extraction function - dispatches to appropriate extractor

    Args:
        filepath: Path to the uploaded file
        file_type: Extension of the file (pdf, docx, txt)

    Returns:
        dict: {"success": True, "text": "..."} or {"success": False, "error": "..."}
    """
    try:
        if file_type == "pdf":
            text = extract_from_pdf(filepath)
        elif file_type == "docx":
            text = extract_from_docx(filepath)
        elif file_type == "txt":
            text = extract_from_txt(filepath)
        else:
            return {"success": False, "error": f"Unsupported file type: {file_type}"}

        if not text:
            return {"success": False, "error": "No text could be extracted from the file"}

        return {"success": True, "text": text}

    except Exception as e:
        return {"success": False, "error": str(e)}
