import PyPDF2
from docx import Document
import io


def extract_text_from_pdf(file_bytes):
    """Extract text from PDF file bytes."""
    try:
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        pages_with_text = 0
        
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                pages_with_text += 1
        
        if pages_with_text == 0:
            raise Exception("No text could be extracted from the PDF. The file may be scanned images or contain no readable text. Please try a different file or use OCR software first.")
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(file_bytes):
    """Extract text from DOCX file bytes."""
    try:
        docx_file = io.BytesIO(file_bytes)
        doc = Document(docx_file)
        
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")


def extract_text_from_txt(file_bytes):
    """Extract text from TXT file bytes."""
    try:
        text = file_bytes.decode('utf-8')
        return text.strip()
    except UnicodeDecodeError:
        try:
            text = file_bytes.decode('latin-1')
            return text.strip()
        except Exception as e:
            raise Exception(f"Error decoding text file: {str(e)}")
    except Exception as e:
        raise Exception(f"Error extracting text from TXT: {str(e)}")


def extract_text(file_bytes, file_type):
    """
    Extract text from uploaded file based on file type.
    
    Args:
        file_bytes: File content as bytes
        file_type: File extension (pdf, docx, txt)
    
    Returns:
        Extracted text as string
    """
    file_type = file_type.lower()
    
    if file_type == 'pdf':
        return extract_text_from_pdf(file_bytes)
    elif file_type in ['docx', 'doc']:
        return extract_text_from_docx(file_bytes)
    elif file_type == 'txt':
        return extract_text_from_txt(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
