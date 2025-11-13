from io import BytesIO
import streamlit as st
from docx import Document
import fitz  # PyMuPDF — VERY fast for PDF (pip install pymupdf)

def extract_text_from_file(uploaded_file):
    """
    Fast, reliable text extraction for PDF, DOCX, TXT.
    Replaces pdfplumber with PyMuPDF for 10x faster PDF extraction.
    """
    text = ""
    name = uploaded_file.name.lower()

    try:
        data = uploaded_file.read()  # read once
        uploaded_file.seek(0)

        # ---------- FAST PDF extraction ----------
        if name.endswith(".pdf"):
            pdf = fitz.open(stream=data, filetype="pdf")
            extracted_chunks = []
            for page in pdf:  # MUCH faster than pdfplumber
                extracted_chunks.append(page.get_text("text"))
            text = "\n".join(extracted_chunks)
            pdf.close()

        # ---------- DOCX extraction ----------
        elif name.endswith(".docx"):
            doc = Document(BytesIO(data))
            text = "\n".join(para.text for para in doc.paragraphs)

        # ---------- TXT extraction ----------
        elif name.endswith(".txt"):
            text = data.decode("utf-8", errors="ignore")

        else:
            st.error("Unsupported file type.")

    except Exception as e:
        st.error(f"❌ Extraction error: {e}")

    return text.strip()
