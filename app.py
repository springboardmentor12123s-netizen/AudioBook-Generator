
import streamlit as st
from core.extractor import extract_texts

st.set_page_config(page_title="AI Audiobook Generator", page_icon="🎧")
st.title("🎧 AI Audiobook Generator — Week 1")

uploaded_files = st.file_uploader(
    "Upload PDF/DOCX/TXT files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    st.subheader("Extracted Text Preview")
    extracted = extract_texts(uploaded_files)

    for name, text in extracted.items():
        st.write(f"**{name}**")
        preview = (text[:2000] + "...") if len(text) > 2000 else text
        st.code(preview or "[No text extracted]")
else:
    st.info("Upload a file to begin.")
