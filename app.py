# app.py
import streamlit as st
import os
import time
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
from extract_text import extract_text
from llm_enrich import enrich_with_prompt
from tts import text_to_audio
from utils import chunk_text

st.set_page_config(page_title="AudioBook Generator", layout="centered")

st.title("📚 AudioBook Generator (Local)")

st.markdown("""
Upload a PDF / DOCX / TXT file. The app will extract text, optionally rewrite it with an LLM (if you set OPENAI_API_KEY),
convert it to speech locally (pyttsx3), and let you play/download the audio — all on your machine.
""")

uploaded = st.file_uploader("Upload PDF / DOCX / TXT", type=['pdf', 'docx', 'txt'])

use_llm = st.checkbox("Use LLM to rewrite text (requires OPENAI_API_KEY)", value=False)

rate = st.slider("Speech rate (words per minute)", min_value=100, max_value=220, value=int(os.getenv("VOICE_RATE",150)))

if uploaded:
    with st.spinner("Extracting text..."):
        try:
            raw_text = extract_text(uploaded)
        except Exception as e:
            st.error(f"Failed to extract text: {e}")
            st.stop()

    st.success("Text extracted.")
    st.text_area("Preview (first 2000 chars)", raw_text[:2000], height=200)

    # chunk text
    chunks = chunk_text(raw_text, max_chars=12000)
    st.write(f"Detected {len(chunks)} chunk(s) to process.")

    step = st.button("Generate Audiobook")
    if step:
        out_base = os.path.join("output", os.path.splitext(uploaded.name)[0])
        os.makedirs("output", exist_ok=True)

        final_audio_paths = []
        progress = st.progress(0)
        for i, chunk in enumerate(chunks):
            pct = int((i / len(chunks)) * 100)
            progress.progress(pct)
            st.info(f"Processing chunk {i+1} / {len(chunks)}")

            # LLM enrichment (optional)
            enriched = chunk
            if use_llm:
                enriched = enrich_with_prompt(chunk)

            # create audio
            chunk_out = f"{out_base}_part{i+1}"
            try:
                out_file = text_to_audio(enriched, chunk_out, prefer_mp3=True, rate=rate)
                final_audio_paths.append(out_file)
            except Exception as e:
                st.error(f"TTS failed for chunk {i+1}: {e}")
                st.stop()
            time.sleep(0.5)

        progress.progress(100)
        st.success("All chunks processed.")

        # If more than 1 part, combine using pydub
        if len(final_audio_paths) > 1:
            try:
                from pydub import AudioSegment
                combined = None
                for p in final_audio_paths:
                    seg = AudioSegment.from_file(p)
                    combined = seg if combined is None else combined + seg
                final_combined = f"{out_base}_full.mp3"
                combined.export(final_combined, format="mp3")
                final_file = final_combined
            except Exception as e:
                st.warning("Combining parts failed; presenting individual part downloads.")
                final_file = None
        else:
            final_file = final_audio_paths[0]

        if final_file:
            st.audio(final_file)
            with open(final_file, "rb") as f:
                btn = st.download_button(
                    label="Download audio",
                    data=f,
                    file_name=os.path.basename(final_file),
                    mime="audio/mpeg"
                )
        else:
            # show the parts individually
            for p in final_audio_paths:
                st.audio(p)
                with open(p,"rb") as f:
                    st.download_button(label=f"Download {os.path.basename(p)}", data=f, file_name=os.path.basename(p))

        st.balloons()