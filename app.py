import streamlit as st
from gtts import gTTS
import pyttsx3
from pydub import AudioSegment
import pdfplumber
from docx import Document
from io import BytesIO
import tempfile
import os
import traceback

st.set_page_config(page_title="AudioBook Generator", page_icon="🎧", layout="wide")
st.title("🎧 AudioBook Generator")
st.write("Upload a document (PDF, DOCX, or TXT) and convert it into an audiobook!")

def extract_text(uploaded_file):
    text = ""
    fname = uploaded_file.name.lower()
    try:
        if fname.endswith(".pdf"):
            file_bytes = uploaded_file.read()
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    p = page.extract_text()
                    if p:
                        text += p + "\n"
            uploaded_file.seek(0)
        elif fname.endswith(".docx"):
            file_bytes = uploaded_file.read()
            doc = Document(BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + "\n"
            uploaded_file.seek(0)
        elif fname.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8", errors="ignore")
            uploaded_file.seek(0)
    except Exception as e:
        st.error(f"Extraction error: {e}")
    return text.strip()

# ----------------------
# Offline TTS using pyttsx3 + pydub (WAV -> MP3)
# ----------------------
def tts_offline_to_mp3(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        temp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name

        engine.save_to_file(text, temp_wav)
        engine.runAndWait()

        # convert wav -> mp3 (pydub requires ffmpeg)
        sound = AudioSegment.from_wav(temp_wav)
        sound.export(temp_mp3, format="mp3")

        # cleanup wav
        try:
            os.remove(temp_wav)
        except:
            pass
        return temp_mp3
    except Exception as e:
        st.error("Offline TTS error: " + str(e))
        st.error(traceback.format_exc())
        return None

# ----------------------
# Online TTS using gTTS
# ----------------------
def tts_gtts_to_mp3(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(temp_path)
        return temp_path
    except Exception as e:
        # show a small message (don’t fail silently)
        st.warning("gTTS failed — falling back to offline TTS. Reason: " + str(e))
        return None

# ----------------------
# Combined wrapper: try online, else offline
# ----------------------
def generate_audio_mp3(text):
    # First try gTTS (online)
    path = tts_gtts_to_mp3(text)
    if path and os.path.exists(path):
        return path

    # If gTTS failed, use offline method
    path = tts_offline_to_mp3(text)
    return path

# ----------------------
# Main UI
# ----------------------
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        text = extract_text(uploaded_file)

    if not text:
        st.error("❌ Could not extract text from the file. Try a different file or use a text file for testing.")
    else:
        st.success("✅ Text extracted successfully!")
        st.text_area("Extracted Text (Preview):", text[:2000], height=250)

        if st.button("🎧 Generate Audio"):
            with st.spinner("Converting text to audio..."):
                audio_path = generate_audio_mp3(text)

            if audio_path and os.path.exists(audio_path):
                st.success("✅ Audio generated successfully!")
                # Show path for debugging (optional)
                st.info(f"Audio file: {audio_path}")

                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()

                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("⬇️ Download Audio File", data=audio_bytes, file_name="audiobook.mp3", mime="audio/mp3")

                # Optionally delete the temp file after use (commented out during debugging)
                try:
                    os.remove(audio_path)
                except:
                    pass
            else:
                st.error("Audio generation failed. Check the logs above.")