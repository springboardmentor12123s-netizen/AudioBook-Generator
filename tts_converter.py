import os
import tempfile
from gtts import gTTS
import pyttsx3
from pathlib import Path

def convert_to_speech(text: str, engine: str = "gTTS (Google)", rate: int = 150, volume: float = 1.0) -> str:
    """
    Convert text to speech using the specified TTS engine.
    
    Args:
        text: The text to convert to speech
        engine: TTS engine to use ("gTTS (Google)" or "pyttsx3 (Offline)")
        rate: Speech rate (for pyttsx3 only)
        volume: Volume level (for pyttsx3 only)
    
    Returns:
        Path to the generated audio file
    """
    
    try:
        # Create a temporary directory for output
        output_dir = tempfile.gettempdir()
        output_file = os.path.join(output_dir, "audiobook.mp3")
        
        if engine == "gTTS (Google)":
            # Use gTTS (Google Text-to-Speech)
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_file)
            return output_file
        
        elif engine == "pyttsx3 (Offline)":
            # Use pyttsx3 (offline TTS)
            engine_obj = pyttsx3.init()
            
            # Set properties
            engine_obj.setProperty('rate', rate)
            engine_obj.setProperty('volume', volume)
            
            # Get available voices and optionally set a specific one
            voices = engine_obj.getProperty('voices')
            if voices:
                # You can select a different voice by index
                # engine_obj.setProperty('voice', voices[0].id)  # First voice
                pass
            
            # Save to file
            engine_obj.save_to_file(text, output_file)
            engine_obj.runAndWait()
            
            return output_file
        
        else:
            raise ValueError(f"Unsupported TTS engine: {engine}")
    
    except Exception as e:
        raise Exception(f"Error converting text to speech: {str(e)}")