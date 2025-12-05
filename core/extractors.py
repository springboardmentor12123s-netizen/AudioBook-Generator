import io
import docx
from pdfplumber import open as pdf_open

# Extract text from PDF bytes
def extract_text_from_pdf_bytes(file_bytes):
    pages = []
    with pdf_open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                pages.append(content)
    return "\n".join(pages)

# Extract text from DOCX bytes
def extract_text_from_docx_bytes(file_bytes):
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

# Extract text from TXT bytes
def extract_text_from_txt_bytes(file_bytes):
    return file_bytes.decode("utf-8", errors="ignore")

# Identify file type and extract text
def extract_text_from_file(uploaded_file):
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    if name.endswith(".pdf"):
        return extract_text_from_pdf_bytes(data)
    elif name.endswith(".docx"):
        return extract_text_from_docx_bytes(data)
    elif name.endswith(".txt"):
        return extract_text_from_txt_bytes(data)

    raise ValueError("Unsupported file format")
