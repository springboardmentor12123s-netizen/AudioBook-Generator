import streamlit as st
from core.extractor import extract_texts
from core.groqres import llm, prompt, generate_script
import json

st.title("Audio book Genrator by Manish Singh")

st.set_page_config(page_title="AI Audiobook Generator", page_icon="🎧")
st.title("🎧 AI Audiobook Generator — Week 1")
File_type = st.selectbox(
    "Select the type of file you want to upload : ",
    ["PDF" , "DOCX" , "TXT"]
)
uploaded_files = st.file_uploader(
    "Upload Any Pdf/Docx/Txt files",
    type=["pdf", "docx" , "txt"],
    accept_multiple_files=True
)
text_extracted = ""
if uploaded_files:
    st.subheader("Extracted Text Preview")
    text_extracted = extract_texts(uploaded_files)

    for name, text in text_extracted.items():
        st.write(f"**{name}**")
        preview = (text[:2000] + "...") if len(text) > 2000 else text
        st.code(preview or "[No text extracted]")
else:
    st.info("Upload a file to begin.")

if text_extracted:
    prompt = st.text_area("Enter your prompt if you want some custom narration or instructions", height=71)
    if st.button("Generate Audiobook Script"):
        st.success("Generating audiobook script...")
        input = str(str(prompt)+" \n" + str(text_extracted))
        # st.write(input)
        response = generate_script(input)
        st.code(response)
        