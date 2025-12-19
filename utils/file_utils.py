"""
file_utils.py
---------------------------------------------
Handles:
- Extracting text from PDF files
- Saving uploaded files safely
---------------------------------------------
"""

import fitz
import docx 
import os

# Opens the PDF document.
# Iterates through each page.
# Extracts text from every page and appends it to a string.
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_text_from_docx(docx_path):                      #Reads text from each paragraph.
    doc = docx.Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs])      #Joins paragraphs with new lines for better readability.

def extract_text_from_txt(txt_path):         #Reads entire content at once.
    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_text_from_file(path):           #Determines file type and calls appropriate extraction function.
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    if ext == ".docx":
        return extract_text_from_docx(path)
    if ext == ".txt":
        return extract_text_from_txt(path)
    raise ValueError("Unsupported file format.")

def save_uploaded_file(uploaded_file, folder="uploads"):  #Saves uploaded file to specified folder.
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
