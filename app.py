import streamlit as st
import os
import tempfile
from modules.text_extraction import TextExtractor
from modules.llm_enrichment import LLMEnrichment
from modules.tts_engine import TTSEngine
from modules.utils import setup_logging
import time

# Setup logging
setup_logging()

# Page configuration
st.set_page_config(
    page_title="Audiobook Generator",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = None
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'enriched_text' not in st.session_state:
    st.session_state.enriched_text = None

def main():
    st.title("📚 Audiobook Generator")
    st.markdown("""
    Convert your documents into engaging audiobooks using AI!
    Upload PDF, DOCX, or TXT files and get a narrated audio version.
    """)
    
    # File upload section
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    # Initialize components
    text_extractor = TextExtractor()
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Process file
        if st.button("Generate Audiobook") or st.session_state.processing_complete:
            with st.spinner("Processing your document..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Step 1: Extract text
                    st.subheader("📖 Text Extraction")
                    with st.status("Extracting text from document...", expanded=True) as status:
                        extracted_text = text_extractor.extract_text(tmp_path)
                        st.session_state.extracted_text = extracted_text
                        st.text_area("Extracted Text", extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text, height=200)
                        status.update(label="Text extraction complete!", state="complete")
                    
                    # Step 2: LLM Enrichment
                    st.subheader("✨ Text Enhancement")
                    with st.status("Enhancing text for narration...", expanded=True) as status:
                        llm_processor = LLMEnrichment()
                        enriched_text = llm_processor.enrich_text(extracted_text)
                        st.session_state.enriched_text = enriched_text
                        st.text_area("Enhanced Text", enriched_text[:1000] + "..." if len(enriched_text) > 1000 else enriched_text, height=200)
                        status.update(label="Text enhancement complete!", state="complete")
                    
                    # Step 3: Text-to-Speech
                    st.subheader("🔊 Audio Generation")
                    with st.status("Converting text to speech...", expanded=True) as status:
                        tts_engine = TTSEngine()
                        
                        # Progress bar for TTS
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.02)  # Simulate progress
                            progress_bar.progress(i + 1)
                        
                        # Generate audio
                        output_file = "audiobook_output.mp3"
                        audio_path = tts_engine.text_to_speech(enriched_text, output_file)
                        st.session_state.audio_file = audio_path
                        
                        # Cleanup
                        tts_engine.cleanup()
                        os.unlink(tmp_path)
                        
                        status.update(label="Audio generation complete!", state="complete")
                    
                    st.session_state.processing_complete = True
                    
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
    
    # Display results
    if st.session_state.processing_complete and st.session_state.audio_file:
        st.header("🎧 Your Audiobook is Ready!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.audio(st.session_state.audio_file, format='audio/mp3')
            
            # Download button
            with open(st.session_state.audio_file, "rb") as file:
                btn = st.download_button(
                    label="Download Audiobook",
                    data=file,
                    file_name="generated_audiobook.mp3",
                    mime="audio/mp3"
                )
        
        with col2:
            st.info("""
            **Next Steps:**
            - Download your audiobook using the button above
            - The audio file is in MP3 format for compatibility
            - You can upload another document to create a new audiobook
            """)
        
        # Reset button
        if st.button("Create New Audiobook"):
            st.session_state.processing_complete = False
            st.session_state.audio_file = None
            st.session_state.extracted_text = None
            st.session_state.enriched_text = None
            st.rerun()

    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This app uses:
        - **Gemini AI** for text enhancement
        - **SpeechT5** for high-quality text-to-speech
        - **GPU Acceleration** for faster processing
        
        **Supported formats:**
        - PDF documents
        - Word documents (.docx)
        - Text files (.txt)
        
        **Note:** For large documents, processing may take several minutes.
        """)
        
        st.header("⚙️ System Info")
        if st.button("Check GPU Status"):
            import torch
            if torch.cuda.is_available():
                st.success(f"GPU: {torch.cuda.get_device_name(0)}")
                st.info(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            else:
                st.warning("GPU not available - using CPU (slower)")

if __name__ == "__main__":
    main()