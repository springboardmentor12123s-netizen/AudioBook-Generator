
# app.py
"""
AudioBook Generator - Final full app.py
Features:
- Fast extraction (PDF via PyMuPDF, DOCX, TXT)
- LLM rewrite options (Gemini cloud or Local quick rewrite)
- Quota-safe Gemini usage with retries & caching
- Translation BEFORE TTS (so selecting Hindi -> text translated to Hindi)
- Multi-language & voice selection (Edge-TTS via modules/tts_engine)
- Saves audio files in generated_audio/
- Attractive UI, About sidebar, paginated history table with play/download
"""

import os
import time
import math
from io import BytesIO
from pathlib import Path
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# load env
load_dotenv()

# fast PDF extraction
import fitz  # PyMuPDF
from docx import Document

# modules (must exist in modules/)
from modules.llm_enrichment import enrich_text_with_gemini_quota_safe, simple_local_enrich
from modules.tts_engine import generate_audio, LANG_VOICES
from modules.translator import translate_text  # translate_text(text, dest_lang)

# Optional: for audio duration reading (mutagen preferred)
try:
    from mutagen.mp3 import MP3
    MUTAGEN_AVAILABLE = True
except Exception:
    MUTAGEN_AVAILABLE = False

# Paths
ROOT = Path.cwd()
AUDIO_DIR = ROOT / "generated_audio"
AUDIO_DIR.mkdir(exist_ok=True, parents=True)

# Sample input path from this session (developer note: treat as test sample)
SAMPLE_FILE_PATH = "/mnt/data/63b135ed-48ed-425d-ad51-7b45732a12ec.png"

# Streamlit page config
st.set_page_config(page_title="AudioBook Generator", page_icon="🎧", layout="wide")
st.title("🎧 AudioBook Generator")
st.caption("Upload → (Optional) Rewrite/Translate → Select language & voice → Generate audio (saved to generated_audio/)")

# Small CSS for nicer look
st.markdown(
    """
    <style>
      .card { background: #fff; padding: 14px; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
      .muted { color: #6c757d; font-size:13px; }
      .mono { font-family: monospace; font-size:13px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Helper: fast extraction
# -------------------------
def extract_text_from_file(uploaded_file, preview_only: bool = False) -> str:
    """Extract text from PDF (PyMuPDF), DOCX or TXT. preview_only reads just first 1-2 pages."""
    name = uploaded_file.name.lower()
    data = uploaded_file.read()
    uploaded_file.seek(0)
    try:
        if name.endswith(".pdf"):
            doc = fitz.open(stream=data, filetype="pdf")
            pages_to_read = min(2, doc.page_count) if preview_only else doc.page_count
            texts = []
            for i in range(pages_to_read):
                page = doc.load_page(i)
                texts.append(page.get_text("text") or "")
            doc.close()
            return "\n\n".join(texts).strip()
        if name.endswith(".docx"):
            docx = Document(BytesIO(data))
            paras = [p.text for p in docx.paragraphs if p.text]
            return "\n\n".join(paras).strip()
        if name.endswith(".txt"):
            return data.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        st.error(f"Extraction error: {e}")
        return ""
    st.error("Unsupported file type.")
    return ""

# -------------------------
# Layout: Sidebar About + Stats
# -------------------------


with st.sidebar:
    # 1. Use a more engaging header with an emoji
    st.header("📚 AudioBook Generator")
    
    # 2. Use st.info or st.success for the main description for a better visual block
    st.info("**Transform documents into multilingual audiobooks with ease.**")
    
    st.markdown("---") # Visual separator
    
    # 3. Enhanced Feature List with icons and bolding
    st.subheader("✨ Key Features")
    st.markdown("""
        * **📤 Upload** PDF, DOCX, or TXT files.
        * **✍️ Optional Rewriting** (using Gemini or a local model).
        * **🌐 Seamless Translation** before Text-to-Speech (TTS).
        * **🎙️ Multi-language Voices** powered by Edge-TTS.
    """)
    
    st.markdown("---") # Visual separator
    
    # 4. Tips section using st.expander or st.warning/st.caption for emphasis
    st.subheader("💡 Tips for Best Results")
    
    # Using an unordered list for better scanning
    st.markdown("""
        * Use **Local Rewrite** for quick, cost-free demos.
        * **Gemini Rewrite** is powerful but consumes API quota; ensure your API key is configured.
    """)

    st.markdown("---") # Final separator
    
    # 5. Author/Credit section using a smaller font (st.caption) or a distinct separator
    st.caption("Developed by Nainsi Verma")
    # Optional: Add a link to a portfolio/GitHub if applicable
    # st.markdown("[GitHub Profile](YOUR_LINK_HERE)")
# -------------------------
# Main UI: two columns
# -------------------------
col_main, col_ctrl = st.columns([3, 1])

# -------------------------
# Main column: upload / rewrite / edit
# -------------------------
with col_main:
    st.markdown("## 1) Upload document")
    uploaded = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf", "docx", "txt"])
    if not uploaded:
        st.info("Upload a file to begin (or use sample file in the sidebar for testing).")
        st.stop()

    # preview extraction
    with st.spinner("Extracting preview..."):
        preview_text = extract_text_from_file(uploaded, preview_only=True)

    if not preview_text:
        st.error("Could not extract preview text.")
        st.stop()

    st.success("Preview extracted.")
    if st.checkbox("Show extracted preview"):
        st.text_area("Preview (first pages)", preview_text, height=220)

    # full extraction (optional)
    full_text = None
    if st.button("Extract full text"):
        with st.spinner("Extracting full text (may take longer for PDFs)..."):
            full_text = extract_text_from_file(uploaded, preview_only=False)
        if full_text:
            st.success("Full text extracted.")
            if st.checkbox("Show full extracted text"):
                st.text_area("Full extracted text", full_text[:25000], height=300)
        else:
            st.error("Full extraction failed.")

    working_text = full_text if full_text else preview_text

    # rewrite options
    st.markdown("## 2) Rewrite (optional)")
    rewrite_mode = st.radio("Rewrite mode", ["No rewrite", "Local quick rewrite", "Gemini (cloud)"], index=1, horizontal=True)
    rewritten_text = working_text

    if rewrite_mode == "Local quick rewrite":
        if st.button("Apply local rewrite"):
            with st.spinner("Applying local rewrite..."):
                rewritten_text = simple_local_enrich(working_text)
            st.success("Local rewrite applied.")
            st.text_area("Rewritten (local) preview", rewritten_text[:20000], height=240)

    elif rewrite_mode == "Gemini (cloud)":
        st.info("Gemini uses API quota; enable only if you have GEMINI_API_KEY configured.")
        preview_only = st.checkbox("Quick preview rewrite (first 3000 chars)", value=True)
        model_choice = st.selectbox("Gemini model", ["models/gemini-2.5-flash", "models/gemini-flash-latest"])
        throttle = st.slider("Throttle (req/min)", 1, 60, 10)
        if st.button("Rewrite with Gemini"):
            text_for_rewrite = working_text[:3000] if preview_only else working_text
            with st.spinner("Rewriting via Gemini (quota-safe)..."):
                rewritten_text = enrich_text_with_gemini_quota_safe(
                    text_for_rewrite,
                    model=model_choice,
                    max_retries_per_chunk=3,
                    throttle_seconds_between_calls=1.2,
                    max_requests_per_minute=throttle,
                    use_local_on_failure=True,
                )
            st.success("Gemini rewrite done.")
            st.text_area("Rewritten (Gemini) preview", rewritten_text[:20000], height=240)

    # editable area
    st.markdown("## 3) Edit text before TTS (optional)")
    edited_text = st.text_area("Text to convert to audio", rewritten_text[:200000], height=300)

# -------------------------
# Controls column: language/voice/generate/history
# -------------------------
with col_ctrl:
    st.markdown("## Controls")
    # language & voice selection
    st.markdown("### Language & Voice")
    available_langs = list(LANG_VOICES.keys())
    LANG_LABELS = {"en": "English", "hi": "Hindi", "fr": "French", "es": "Spanish", "ta": "Tamil", "te": "Telugu"}
    lang = st.selectbox("Language", options=available_langs, format_func=lambda x: LANG_LABELS.get(x, x))

    voices = LANG_VOICES.get(lang, [])
    if voices:
        voice_labels = [v[1] for v in voices]
        voice_ids = [v[0] for v in voices]
        idx = st.selectbox("Voice", options=list(range(len(voice_labels))), format_func=lambda i: voice_labels[i])
        selected_voice = voice_ids[idx]
    else:
        selected_voice = None

    st.markdown("---")
    st.markdown("### Generate audio")
    # translate before TTS
    if st.button("🎧 Generate Audio", use_container_width=True):
        if not edited_text.strip():
            st.error("No text to convert.")
        else:
            # 1) Translate if target language not English
            if lang != "en":
                with st.spinner(f"Translating to {LANG_LABELS.get(lang)}..."):
                    text_for_tts = translate_text(edited_text, dest_lang=lang)
            else:
                text_for_tts = edited_text

            # preview translation option
            if lang != "en" and st.checkbox("Show translated text preview"):
                st.text_area("Translated text preview", text_for_tts[:3000], height=200)

            # 2) Generate audio (Edge-TTS) and save file
            with st.spinner("Generating audio (Edge-TTS)... This may take a few seconds depending on length."):
                try:
                    audio_path, mime = generate_audio(text_for_tts, lang=lang, voice=selected_voice)
                except Exception as e:
                    st.error(f"Audio generation error: {e}")
                    audio_path, mime = None, None

            if audio_path and os.path.exists(audio_path):
                st.success("Audio generated & saved!")
                # play + download
                with open(audio_path, "rb") as fh:
                    audio_bytes = fh.read()
                st.audio(audio_bytes, format=mime)
                st.download_button("⬇ Download MP3", data=audio_bytes, file_name=os.path.basename(audio_path), mime=mime)
                st.markdown(f"Saved: `{audio_path}`")
            else:
                st.error("Audio generation failed. Check server logs.")

    st.markdown("---")
    # -------------------------
    # Paginated History table
    # -------------------------
    st.markdown("## Generated Audio History")
    files = sorted(AUDIO_DIR.glob("*.mp3"), key=os.path.getmtime, reverse=True)
    if not files:
        st.info("No generated audio files yet.")
    else:
        page_size = 5
        total = len(files)
        total_pages = max(1, math.ceil(total / page_size))
        # maintain page in session state
        if "history_page" not in st.session_state:
            st.session_state["history_page"] = 1
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=st.session_state["history_page"], step=1)
        st.session_state["history_page"] = page

        start = (page - 1) * page_size
        page_files = files[start:start + page_size]

        # build table rows
        rows = []
        for f in page_files:
            name = f.name
            created = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            duration = "N/A"
            if MUTAGEN_AVAILABLE:
                try:
                    mp = MP3(f)
                    seconds = int(mp.info.length)
                    mins = seconds // 60
                    secs = seconds % 60
                    duration = f"{mins:02d}:{secs:02d}"
                except Exception:
                    duration = "N/A"
            rows.append({"File Name": name, "Created": created})
        st.table(rows)

        # play / download controls per file
        for f in page_files:
            cols = st.columns([3, 1])
            with cols[0]:
                st.write(f"🎧 {f.name}")
            with cols[1]:
                if st.button("▶ Play", key=f"play_{f.name}"):
                    with open(f, "rb") as fh:
                        st.audio(fh.read(), format="audio/mp3")
                if st.button("⬇", key=f"dl_{f.name}"):
                    with open(f, "rb") as fh:
                        st.download_button("Download", data=fh.read(), file_name=f.name, mime="audio/mp3", key=f"dlbtn_{f.name}")

# Footer / About modal (collapsible)
st.markdown("---")
st.markdown("Developed by Nainsi Verma. ❤️")
with st.expander("About"):
    st.markdown("""
    **AudioBook Generator** is an open-source Streamlit app that converts documents (PDF, DOCX, TXT) into multilingual audiobooks.
    
    Features include:
    - Fast text extraction using PyMuPDF for PDFs.
    - Optional rewriting using Gemini (cloud) or a local quick rewrite.
    - Translation to multiple languages before Text-to-Speech (TTS).
    - Multi-language voice selection powered by Edge-TTS.
    
    Developed by Nainsi Verma. Contributions and feedback are welcome!
    """)