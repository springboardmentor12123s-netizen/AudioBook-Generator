import streamlit as st
import os
from pathlib import Path
import tempfile
from extract import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from llm_enrichment import enrich_text_with_llm
from tts_converter import convert_to_speech
import traceback

# Page Configuration
st.set_page_config(
    page_title="Professional AudioBook Generator | AI-Powered",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(120deg, #2E86AB, #A23B72, #F18F01);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2.5rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<h1 class="main-title">🎧 Professional AudioBook Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your documents into engaging audiobooks using advanced AI technology</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Configuration Panel")
    st.markdown("---")
    
    # LLM Provider
    st.markdown("#### AI Text Enhancement")
    llm_provider = st.selectbox(
        "Language Model Provider",
        ["OpenAI (GPT-3.5)", "OpenAI (GPT-4)", "Google Gemini (1.5)", "Skip Enrichment"],
        help="Select AI model for text enhancement"
    )
    
    # API Key
    if llm_provider != "Skip Enrichment":
        api_key_label = "OpenAI API Key" if "OpenAI" in llm_provider else "Gemini API Key"
        api_key = st.text_input(
            api_key_label,
            type="password",
            help="Enter your API key for the selected provider"
        )
    else:
        api_key = None
    
    st.markdown("---")
    
    # TTS Engine
    st.markdown("#### Text-to-Speech Engine")
    tts_engine = st.selectbox(
        "Voice Synthesis Engine",
        ["gTTS (Google)", "pyttsx3 (Offline)"],
        help="Choose between online (higher quality) or offline (privacy) TTS"
    )
    
    # Voice Settings for pyttsx3
    if tts_engine == "pyttsx3 (Offline)":
        st.markdown("##### Voice Settings")
        voice_rate = st.slider("Speech Rate (WPM)", 100, 300, 150, help="Words per minute")
        voice_volume = st.slider("Volume Level", 0.0, 1.0, 1.0, step=0.1)
    else:
        voice_rate = 150
        voice_volume = 1.0
    
    st.markdown("---")
    
    # Quick Guide
    with st.expander("📚 Quick Start Guide"):
        st.markdown("""
        1. **Upload** - Select your document files
        2. **Configure** - Choose AI model and voice settings
        3. **Generate** - Click the generate button
        4. **Download** - Save your audiobook
        """)

# Main Content Area
tab1, tab2, tab3 = st.tabs(["📤 Upload Documents", "📊 Features", "ℹ️ Information"])

with tab1:
    st.markdown("### Upload Your Documents")
    st.markdown("Supported formats: **PDF**, **DOCX**, **TXT**")
    
    uploaded_files = st.file_uploader(
        "Choose files to convert",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple files at once"
    )
    
    if uploaded_files:
        st.success(f"✅ Successfully uploaded {len(uploaded_files)} file(s)")
        
        with st.expander("📋 View uploaded files"):
            for idx, file in enumerate(uploaded_files, 1):
                st.write(f"{idx}. **{file.name}** ({file.size:,} bytes)")

with tab2:
    st.markdown("### ✨ Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>🤖 AI-Powered Enhancement</h4>
            <p>Leverages GPT-3.5, GPT-4, or Gemini to rewrite text for natural audio narration</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>🎵 High-Quality Audio</h4>
            <p>Professional text-to-speech with customizable voice settings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>📚 Multi-Format Support</h4>
            <p>Process PDF, DOCX, and TXT files seamlessly</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>⚡ Batch Processing</h4>
            <p>Convert multiple documents in a single operation</p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### ℹ️ About This Application")
    st.info("""
    **AudioBook Generator** is an advanced document-to-audio conversion tool that combines:
    - State-of-the-art AI language models for text optimization
    - Professional-grade text-to-speech synthesis
    - Intuitive user interface for seamless experience
    
    Perfect for creating audiobooks, study materials, accessibility content, and more.
    """)

# Generate Button and Processing
st.markdown("---")

if uploaded_files:
    generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
    with generate_col2:
        generate_button = st.button(
            "🎵 Generate AudioBook",
            type="primary",
            use_container_width=True
        )
else:
    st.warning("⚠️ Please upload at least one document to proceed")
    generate_button = False

if generate_button:
    # Validation
    if llm_provider != "Skip Enrichment" and not api_key:
        st.error("❌ Please enter your API key in the sidebar configuration panel")
    else:
        # Progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Text Extraction
            status_text.markdown("**Step 1/4:** 📄 Extracting text from documents...")
            all_text = ""
            
            for idx, uploaded_file in enumerate(uploaded_files):
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                
                file_extension = Path(uploaded_file.name).suffix.lower()
                
                try:
                    if file_extension == ".pdf":
                        text = extract_text_from_pdf(tmp_file_path)
                    elif file_extension == ".docx":
                        text = extract_text_from_docx(tmp_file_path)
                    elif file_extension == ".txt":
                        text = extract_text_from_txt(tmp_file_path)
                    else:
                        st.warning(f"⚠️ Unsupported file type: {uploaded_file.name}")
                        continue
                    
                    all_text += f"\n\n=== {uploaded_file.name} ===\n\n{text}"
                except Exception as e:
                    st.warning(f"⚠️ Error extracting {uploaded_file.name}: {str(e)}")
                finally:
                    os.unlink(tmp_file_path)
                
                progress_bar.progress((idx + 1) / (len(uploaded_files) * 4))
            
            if not all_text.strip():
                st.error("❌ No text could be extracted from the uploaded files")
            else:
                with st.expander("📖 Preview extracted text"):
                    st.text_area("Raw Text", all_text[:500] + "..." if len(all_text) > 500 else all_text, height=150)
                
                # Step 2: AI Enhancement
                if llm_provider != "Skip Enrichment":
                    status_text.markdown("**Step 2/4:** 🤖 Enhancing text with AI...")
                    progress_bar.progress(0.5)
                    
                    try:
                        enriched_text = enrich_text_with_llm(all_text, llm_provider, api_key)
                        with st.expander("✨ Preview enriched text"):
                            st.text_area("AI-Enhanced Text", enriched_text[:500] + "..." if len(enriched_text) > 500 else enriched_text, height=150)
                    except Exception as e:
                        st.warning(f"⚠️ Enhancement error: {str(e)}")
                        st.info("💡 Continuing with original text...")
                        enriched_text = all_text
                else:
                    enriched_text = all_text
                    progress_bar.progress(0.5)
                
                # Step 3: Text-to-Speech
                status_text.markdown("**Step 3/4:** 🎙️ Converting to speech...")
                progress_bar.progress(0.75)
                
                try:
                    audio_file_path = convert_to_speech(enriched_text, tts_engine, voice_rate, voice_volume)
                    
                    # Step 4: Complete
                    status_text.markdown("**Step 4/4:** ✅ Processing complete!")
                    progress_bar.progress(1.0)
                    
                    st.success("🎉 Your audiobook has been generated successfully!")
                    
                    # Display audio player
                    st.audio(audio_file_path, format='audio/mp3')
                    
                    # Download button
                    with open(audio_file_path, 'rb') as audio_file:
                        st.download_button(
                            label="⬇️ Download AudioBook (MP3)",
                            data=audio_file,
                            file_name="audiobook.mp3",
                            mime="audio/mp3",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Text-to-speech error: {str(e)}")
                    st.error(traceback.format_exc())
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.error(traceback.format_exc())
        finally:
            progress_bar.empty()
            status_text.empty()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Professional AudioBook Generator</strong> | Powered by AI Technology</p>
    <p style='font-size: 0.9rem;'>Built with Streamlit • OpenAI • Google Gemini • gTTS</p>
</div>
""", unsafe_allow_html=True)