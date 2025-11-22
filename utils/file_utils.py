"""
file_utils.py
---------------------------------------------
Handles:
- Extracting text from PDF files
- Saving uploaded files safely
---------------------------------------------
"""

import fitz  # PyMuPDF (fast and accurate PDF text extractor)
import os


# ------------------------------------------------------
# PDF → TEXT EXTRACTION
# ------------------------------------------------------
def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of the PDF.

    Parameters:
        pdf_path (str): Path to PDF file.

    Returns:
        text (str): Extracted text from the PDF.
    """

    text = ""

    try:
        # Open the PDF file
        pdf = fitz.open(pdf_path)

        # Loop through all pages
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text() + "\n"

        pdf.close()

    except Exception as e:
        return f"Error reading PDF: {str(e)}"

    # Return the raw text
    return text.strip()


# ------------------------------------------------------
# SAVE UPLOADED FILES SAFELY
# ------------------------------------------------------
def save_uploaded_file(uploaded_file, folder="audio_uploads"):
    """
    Saves an uploaded file to a specific folder.

    Parameters:
        uploaded_file: File uploaded from Streamlit file uploader.
        folder (str): Folder where file should be saved.

    Returns:
        file_path (str): Path where file is saved.
    """

    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
