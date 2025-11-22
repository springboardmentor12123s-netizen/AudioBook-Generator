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

from utils.file_utils import extract_text_from_pdf, save_uploaded_file


# ------------------------------------------------------
# Save uploaded file
# ------------------------------------------------------
def save_file(uploaded_file, folder="audio_uploads"):
    """
    Wrapper for save_uploaded_file().

    Parameters:
        uploaded_file: File uploaded from Streamlit UI.
        folder (str): Folder to save file in.

    Returns:
        file_path (str): Path where file was saved.
    """
    return save_uploaded_file(uploaded_file, folder)


# ------------------------------------------------------
# Extract text from a PDF file
# ------------------------------------------------------
def get_pdf_text(pdf_path):
    """
    Wrapper for extract_text_from_pdf().

    Parameters:
        pdf_path (str): Path to a stored PDF file.

    Returns:
        text (str): Extracted text from the PDF.
    """
    return extract_text_from_pdf(pdf_path)
