import streamlit as st
import os
from text_extractor import extract_text
from llm_enhancer import enhance_text_for_audiobook
from tts_generator import generate_audio_from_text, get_supported_languages

st.set_page_config(page_title="AudioBook Generator",
                   page_icon="🎧",
                   layout="wide")

st.title("🎧 AudioBook Generator")
st.markdown("""
Transform your documents into engaging audiobooks using AI-powered text enhancement and text-to-speech technology.

Upload your PDF, DOCX, or TXT files and get a professionally narrated audiobook in minutes!
""")

# Sidebar for settings
st.sidebar.header("Settings")
language_options = get_supported_languages()
selected_language = st.sidebar.selectbox(
    "Select Language",
    options=list(language_options.keys()),
    format_func=lambda x: f"{language_options[x]} ({x})",
    index=list(language_options.keys()).index('en')
    if 'en' in language_options else 0)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### How it works:
1. **Upload** your document(s)
2. **Extract** text from files
3. **Enhance** with AI narration style
4. **Generate** high-quality audio
5. **Download** your audiobook
""")

# File uploader
uploaded_files = st.file_uploader(
    "Upload your documents",
    type=['pdf', 'docx', 'txt'],
    accept_multiple_files=True,
    help="You can upload multiple files. Supported formats: PDF, DOCX, TXT")

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")

    # Display uploaded files
    with st.expander("View uploaded files"):
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({file.size / 1024:.2f} KB)")

    # Generate audiobook button
    if st.button("🎬 Generate Audiobook",
                 type="primary",
                 use_container_width=True):
        try:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()

            all_text = ""

            # Step 1: Extract text from all files
            status_text.text("📖 Extracting text from documents...")
            for i, uploaded_file in enumerate(uploaded_files):
                file_bytes = uploaded_file.read()
                file_type = uploaded_file.name.split('.')[-1]

                with st.spinner(
                        f"Extracting text from {uploaded_file.name}..."):
                    extracted_text = extract_text(file_bytes, file_type)
                    all_text += f"\n\n{extracted_text}"

                progress_bar.progress((i + 1) / (len(uploaded_files) * 3))

            st.success(
                f"✅ Extracted {len(all_text)} characters from {len(uploaded_files)} file(s)"
            )

            # Show extracted text preview
            with st.expander("Preview extracted text"):
                st.text_area("Extracted Content",
                             all_text[:1000] +
                             "..." if len(all_text) > 1000 else all_text,
                             height=200)

            # Step 2: Enhance text with LLM
            status_text.text(
                "✨ Enhancing text for audiobook narration with Google Gemini AI..."
            )
            progress_bar.progress(0.4)

            with st.spinner(
                    "Google Gemini AI is rewriting your text for engaging narration..."
            ):
                enhanced_text = enhance_text_for_audiobook(all_text)

            progress_bar.progress(0.7)
            st.success("✅ Text enhanced for audiobook narration")

            # Show enhanced text preview
            with st.expander("Preview enhanced text"):
                st.text_area(
                    "Enhanced Content",
                    enhanced_text[:1000] +
                    "..." if len(enhanced_text) > 1000 else enhanced_text,
                    height=200)

            # Step 3: Generate audio
            status_text.text("🎤 Converting text to speech...")

            with st.spinner(
                    "Generating audio file... This may take a few minutes for long texts."
            ):
                # Create filename based on first uploaded file
                base_filename = uploaded_files[0].name.rsplit('.', 1)[0]
                output_filename = f"{base_filename}_audiobook.mp3"

                audio_path = generate_audio_from_text(
                    enhanced_text,
                    output_filename=output_filename,
                    language=selected_language or 'en')

            progress_bar.progress(1.0)
            status_text.text("✅ Audiobook generation complete!")

            st.success("🎉 Your audiobook is ready!")

            # Display audio player
            st.subheader("🎧 Preview Your Audiobook")
            with open(audio_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')

            # Download button
            st.download_button(label="⬇️ Download Audiobook (MP3)",
                               data=audio_bytes,
                               file_name=output_filename,
                               mime="audio/mp3",
                               use_container_width=True)

            # Show file info
            file_size_mb = len(audio_bytes) / (1024 * 1024)
            st.info(
                f"📊 Audio file size: {file_size_mb:.2f} MB | Language: {language_options[selected_language]}"
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.error("Please check your files and try again.")

else:
    st.info("👆 Upload one or more documents to get started!")

    # Example section
    st.markdown("---")
    st.subheader("📚 Supported Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **📄 Multiple Formats**
        - PDF documents
        - DOCX files
        - Plain text files
        """)

    with col2:
        st.markdown("""
        **🤖 AI Enhancement**
        - Natural narration flow
        - Engaging storytelling
        - Professional quality
        """)

    with col3:
        st.markdown("""
        **🎵 Audio Output**
        - High-quality MP3
        - Multiple languages
        - Instant download
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
    <small>Built with Streamlit, Google Gemini, and gTTS | Transform your reading into listening</small>
    </div>
    """,
            unsafe_allow_html=True)
