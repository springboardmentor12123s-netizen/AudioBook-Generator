import os
import tempfile
import streamlit as st
from io import BytesIO

from utils.file_utils import extract_text_from_file, ALLOWED_EXTENSIONS
from utils.llm_utils import summarize_with_openai, summarize_with_transformers, llm_available_openai, llm_available_transformers
from utils.tts_utils import tts_gtts_save, tts_pyttsx3_save

# ---------------- Page config ----------------
st.set_page_config(page_title="AI Audiobook Generator ", layout="wide", page_icon="🎧")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3208/3208751.png", width=80)
    st.title("🎧 Audiobook Generator")
    st.markdown(" — Summarize & Generate Voice")
    st.divider()

    # LLM choice
    st.markdown("### 🔮 Summarization (LLM)")
    llm_choice = st.selectbox("Choose summarization backend", ["OpenAI (API)", "Transformers (local)"])
    openai_key = None
    if llm_choice == "OpenAI (API)":
        openai_key = st.text_input("OpenAI API Key (or set OPENAI_API_KEY env)", type="password")
    summary_length = st.slider("Target summary length (approx words)", min_value=30, max_value=800, value=150, step=10)

    st.divider()
    st.markdown("### 🔊 Text-to-Speech (TTS)")
    tts_choice = st.selectbox("TTS engine", ["gTTS (online, MP3)", "pyttsx3 (offline, WAV)"])
    tts_lang = st.text_input("TTS language code (gTTS)", value="en")
    st.divider()

    st.markdown("### ⚙️ Advanced")
    preview_len = st.slider("Preview chars before summary", 200, 5000, 1500, step=100)
    st.caption("Transformers will attempt to load a summarization model (heavy).")

st.write("# AI Audiobook Generator — Week 2")
st.write("Upload a file, extract text, summarize it with an LLM, and generate audio.")

# ---------------- Upload ----------------
uploaded_file = st.file_uploader("Upload PDF / DOCX / TXT", type=list(ALLOWED_EXTENSIONS))
if not uploaded_file:
    st.info("Upload a file to begin. Try files in sample_files/ or drag & drop here.")
    st.stop()

# ---------------- Extract ----------------
file_bytes = uploaded_file.read()
with st.spinner("Extracting text..."):
    try:
        text, meta = extract_text_from_file(uploaded_file.name, file_bytes)
    except Exception as e:
        st.error(f"Failed to extract text: {e}")
        st.stop()

st.success("Text extracted ✅")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Extracted Text (preview)")
    st.text_area("extracted", value=(text[:preview_len] + ("\n\n... [truncated]" if len(text) > preview_len else "")), height=300)

with col2:
    with st.expander("File metadata"):
        st.json(meta)
    st.download_button("Download full extracted text", data=BytesIO(text.encode("utf-8")).getvalue(),
                       file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_extracted.txt",
                       mime="text/plain")

st.write("---")

# ---------------- Summarize ----------------
st.subheader("Summarize")
do_summary = st.button("📝 Generate Summary")

summary_text = None
if do_summary:
    # Prefer env var if not entered
    if llm_choice == "OpenAI (API)":
        key = openai_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            st.error("OpenAI API key required for this option. Set OPENAI_API_KEY envvar or paste it in the sidebar.")
        else:
            with st.spinner("Summarizing with OpenAI..."):
                try:
                    summary_text = summarize_with_openai(text, key, max_words=summary_length)
                except Exception as e:
                    st.error(f"OpenAI summarization failed: {e}")
    else:
        # transformers path
        if not llm_available_transformers():
            st.error("Transformers summarizer not available. Install `transformers` and `torch` to use local summarization.")
        else:
            with st.spinner("Summarizing with local transformer model... (may take time)"):
                try:
                    summary_text = summarize_with_transformers(text, max_words=summary_length)
                except Exception as e:
                    st.error(f"Local summarization failed: {e}")

if summary_text:
    st.success("Summary generated ✅")
    st.subheader("Summary")
    st.write(summary_text)
    st.download_button("Download summary (.txt)", data=BytesIO(summary_text.encode("utf-8")).getvalue(),
                       file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_summary.txt",
                       mime="text/plain")
else:
    st.info("Generate a summary to see results here.")

st.write("---")

# ---------------- TTS ----------------
st.subheader("Generate Audio (TTS)")
st.markdown("Use the summary (recommended) or the full extracted text. Choose engine and click `Generate Audio`.")

tts_source = st.radio("Audio source", ["Summary (if present)", "Full extracted text"], index=0)
generate_audio = st.button("🔊 Generate Audio")

if generate_audio:
    source_text = summary_text if tts_source.startswith("Summary") and summary_text else text
    if not source_text or len(source_text.strip()) == 0:
        st.error("No text to synthesize.")
    else:
        with st.spinner("Generating audio..."):
            try:
                if tts_choice == "gTTS (online, MP3)":
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tts_gtts_save(source_text, tmp.name, lang=tts_lang)
                    audio_bytes = open(tmp.name, "rb").read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("Download MP3", data=audio_bytes, file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_audio.mp3", mime="audio/mpeg")
                else:
                    # pyttsx3 offline -> produce WAV
                    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                    tts_pyttsx3_save(source_text, tmp.name)
                    audio_bytes = open(tmp.name, "rb").read()
                    st.audio(audio_bytes, format="audio/wav")
                    st.download_button("Download WAV", data=audio_bytes, file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_audio.wav", mime="audio/wav")
                st.success("Audio generated ✅")
            except Exception as e:
                st.error(f"TTS failed: {e}")
