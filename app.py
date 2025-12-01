import os
import streamlit as st

from core.extract_text import extract_text_from_files
from core.enrich_text import rewrite_for_audiobook
from core.tts_engine import text_to_speech

# ----- Page config -----
st.set_page_config(
    page_title="AI AudioBook Generator",
    layout="wide",
)

# ----- Global styling: white bg, dark text, large font -----
st.markdown(
    """
    <style>
    .main {
        background-color: #ffffff;
        color: #111111;
    }
    .block-container {
        max-width: 1100px;
        margin: 0 auto;
        padding-top: 1.5rem;
    }
    [data-testid="stSidebar"] {
        background-color: #f2f4ff;
        color: #111111;
        border-right: 1px solid #e5e7eb;
    }
    [data-testid="stSidebar"] * {
        color: #111111 !important;
        font-size: 19px !important;
    }

    html, body, [class*="css"]  {
        font-size: 22px !important;
    }
    textarea {
        font-size: 20px !important;
    }

    .section-card {
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        border-radius: 0.9rem;
        background-color: #fafafa;
        border: 1px solid #e5e7eb;
    }
    .section-title {
        font-weight: 700;
        font-size: 26px;
        color: #111111;
        margin-bottom: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----- Sidebar -----
with st.sidebar:
    st.markdown("## Settings")
    st.write("Control how the audiobook is generated.")
    lang = st.selectbox("Language", ["en"], index=0)
    slow = st.checkbox("Slow narration", value=False, help="Enable for slightly slower speech.")
    st.markdown("---")
    st.markdown("### Steps to use")
    st.markdown("1. Upload documents\n\n2. Extract text\n\n3. Rewrite text\n\n4. Generate audio")

# ----- Header -----
st.markdown("<h1 style='color:#2563eb; text-align:center;'>AI AudioBook Generator</h1>", unsafe_allow_html=True)
st.caption(
    "Upload PDF, DOCX, or TXT files and turn them into an audiobook using AI-style rewriting and Text-to-Speech."
)

# ----- Session state -----
for key in ["raw_text", "enriched_text", "audio_path"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# ----- 1. Upload & extract -----
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">1. Upload documents</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Supported formats: PDF, DOCX, TXT",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="You can upload one or more documents.",
)

if uploaded_files and st.button("Extract text", use_container_width=True):
    with st.spinner("Extracting text from uploaded files..."):
        extracted = extract_text_from_files(uploaded_files)
    st.session_state.raw_text = extracted
    if extracted:
        st.success("Text extracted successfully.")
    else:
        st.warning("No readable text found in the uploaded files.")
st.markdown("</div>", unsafe_allow_html=True)

# ----- 2. Show extracted text -----
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">2. Extracted text</div>', unsafe_allow_html=True)
st.text_area(
    "Raw extracted text",
    value=st.session_state.raw_text,
    height=260,
    placeholder="After extraction, the plain text from your documents will appear here.",
)
st.markdown("</div>", unsafe_allow_html=True)

# ----- 3. Rewrite text -----
if st.session_state.raw_text:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">3. Prepare audiobook text</div>', unsafe_allow_html=True)
    if st.button("Rewrite for audiobook (demo)", use_container_width=True):
        with st.spinner("Preparing audiobook-style narration..."):
            enriched = rewrite_for_audiobook(st.session_state.raw_text)
        st.session_state.enriched_text = enriched
        st.success("Audiobook text is ready.")
    st.text_area(
        "Audiobook-style text (demo)",
        value=st.session_state.enriched_text,
        height=260,
        placeholder="The rewritten text for narration will appear here.",
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ----- 4. Generate audio -----
if st.session_state.enriched_text:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">4. Generate audio</div>', unsafe_allow_html=True)
    if st.button("Generate audio with gTTS", use_container_width=True):
        with st.spinner("Generating audio file..."):
            outputs_dir = "outputs"
            os.makedirs(outputs_dir, exist_ok=True)
            out_path = os.path.join(outputs_dir, "audiobook_demo.mp3")
            text_to_speech(
                st.session_state.enriched_text,
                out_path,
                lang=lang,
                slow=slow,
            )
            st.session_state.audio_path = out_path
        st.success("Audio generated successfully.")

    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        with open(st.session_state.audio_path, "rb") as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format="audio/mp3")
        st.download_button(
            "Download audiobook",
            data=audio_bytes,
            file_name="audiobook_demo.mp3",
            mime="audio/mp3",
            use_container_width=True,
        )
    else:
        st.info("Generate the audio to preview and download it here.")
    st.markdown("</div>", unsafe_allow_html=True)
