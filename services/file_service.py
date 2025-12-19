"""
file_service.py
------------------------------------------------------
This service layer handles:
- Saving uploaded files (PDF, audio, etc.)
- Extracting text from PDF files

Purpose:
--------
Keeping file operations separate from the main `app.py`
makes the project:
- Cleaner
- Easier to maintain
- More professional
- Simple for mentor to review

This file simply wraps the utility functions.
------------------------------------------------------
"""

import os
from utils.file_utils import extract_text_from_file, save_uploaded_file

def save_file(uploaded_file, folder="uploads"):
    return save_uploaded_file(uploaded_file, folder)

def extract_text(file_path):
    return extract_text_from_file(file_path)

def get_pdf_text(pdf_path):
    return extract_text_from_file(pdf_path)
