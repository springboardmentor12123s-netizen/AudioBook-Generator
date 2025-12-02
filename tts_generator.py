from gtts import gTTS
import os


def generate_audio_from_text(text, output_filename="audiobook.mp3", language='en'):
    """
    Convert text to speech using gTTS and save as MP3 file.
    Args:
        text: The text to convert to speech
        output_filename: Name of the output audio file
        language: Language code for TTS (default: 'en' for English)
    Returns:
        Path to the generated audio file
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("No text provided for audio generation")
    
    try:
        # Create a temporary directory for audio files if it doesn't exist
        audio_dir = "generated_audio"
        os.makedirs(audio_dir, exist_ok=True)
        
        # Full path for the output file
        output_path = os.path.join(audio_dir, output_filename)
        
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Save the audio file
        tts.save(output_path)
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Error generating audio: {str(e)}")


def get_supported_languages():
    """
    Get a dictionary of supported languages for gTTS.
    
    Returns:
        Dictionary of language codes and names
    """
    from gtts.lang import tts_langs
    return tts_langs()
