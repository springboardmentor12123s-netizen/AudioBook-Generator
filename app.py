import streamlit as st
import llm
import utils

st.set_page_config(page_title="AI AudioBook Generator", page_icon="🎧", layout="wide")

if not llm.configure_openrouter():
    st.stop()

st.sidebar.title("Configuration")

uploaded_file = st.sidebar.file_uploader("1. Upload Document", type=["pdf", "docx", "txt"])

tts_engine = st.sidebar.selectbox(
    "2. Choose Audio Engine",
    ("gTTS (Online - Supports Telugu/Hindi)", "System Voice (Offline - English Only)")
)
lang_code = 'en'
lang_name = 'English'

if tts_engine == "gTTS (Online - Supports Telugu/Hindi)":
    LANGUAGES = {
        "English": "en",
        "Telugu": "te",
        "Hindi": "hi",
        "Tamil": "ta",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Spanish": "es",
        "French": "fr"
    }
    lang_name = st.sidebar.selectbox("3. Select Output Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[lang_name]
else:
    st.sidebar.info("Offline mode supports English. For Telugu, use gTTS.")

generate_btn = st.sidebar.button("Generate Audiobook", type="primary")

st.title("🎧 AI AudioBook Generator")

if "extracted" not in st.session_state:
    st.session_state.extracted = None
    st.session_state.enriched = None
    st.session_state.translated = None
    st.session_state.audio = None

if uploaded_file and not st.session_state.extracted:
    with st.spinner("Reading file..."):
        st.session_state.extracted = utils.extract_text(uploaded_file)
        if st.session_state.extracted:
            st.success("File read successfully!")

if generate_btn and st.session_state.extracted:
    
    with st.spinner("Refining text with AI (English)..."):
        st.session_state.enriched = llm.enrich_text_in_english(st.session_state.extracted)
    
    final_script = st.session_state.enriched
    if lang_code != 'en' and final_script:
        with st.spinner(f"Translating to {lang_name}..."):

            st.session_state.translated = utils.translate_text(final_script, lang_code)
            final_script = st.session_state.translated
    else:
        st.session_state.translated = final_script

    if final_script:
        with st.spinner(f"Generating Audio in {lang_name}..."):
            if tts_engine.startswith("gTTS"):
                st.session_state.audio = utils.convert_text_to_speech_gtts(final_script, lang_code)
            else:
                st.session_state.audio = utils.convert_text_to_speech_pyttsx3(final_script)

tab1, tab2, tab3 = st.tabs(["📄 Original Text", "📝 Final Script", "🎧 Audio Player"])

with tab1:
    if st.session_state.extracted:
        st.text_area("Original Text", st.session_state.extracted, height=400, label_visibility="collapsed")
    else:
        st.info("Upload a file to see text.")

with tab2:
    if st.session_state.translated and lang_code != 'en':
        st.subheader(f"Script ({lang_name})")
        st.text_area("Translated Script", st.session_state.translated, height=400, label_visibility="collapsed")
    elif st.session_state.enriched:
        st.subheader("Script (English)")
        st.text_area("Enriched Script", st.session_state.enriched, height=400, label_visibility="collapsed")
    else:
        st.info("Generate audio to see the script.")

with tab3:
    if st.session_state.audio:
        st.audio(st.session_state.audio, format="audio/mp3")
        st.download_button("Download MP3", st.session_state.audio, "audiobook.mp3", "audio/mp3")
        st.success(f"Playing in {lang_name}!")
    else:
        st.info("Generate audio to listen.")
