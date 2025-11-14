import pyttsx3
import os
import logging
from threading import Thread
import time

class TTSEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_pyttsx3()
    
    def _setup_pyttsx3(self):
        """Setup pyttsx3 TTS engine"""
        try:
            self.engine = pyttsx3.init()
            
            # Set properties for better audio quality
            self.engine.setProperty('rate', 180)  # Speaking speed
            self.engine.setProperty('volume', 0.8)  # Volume level
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            self.logger.info(f"Available voices: {len(voices)}")
            
            # Try to use a better voice if available
            if len(voices) > 1:
                # Prefer female voice usually at index 1
                self.engine.setProperty('voice', voices[1].id)
            
            self.logger.info("pyttsx3 TTS engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to setup pyttsx3: {str(e)}")
            # Try alternative initialization
            try:
                self.engine = pyttsx3.init(driverName='sapi5')
                self.engine.setProperty('rate', 180)
                self.engine.setProperty('volume', 0.8)
                self.logger.info("pyttsx3 initialized with sapi5 driver")
            except:
                raise Exception(f"Could not initialize TTS engine: {str(e)}")
    
    def text_to_speech(self, text: str, output_path: str = "output.mp3") -> str:
        """
        Convert text to speech using pyttsx3 and save as WAV file
        Note: pyttsx3 can only save as WAV directly, but we can rename to .mp3
        """
        try:
            # For simplicity, let's process the entire text at once
            # pyttsx3 can handle reasonably long texts
            
            # Save directly as WAV file (pyttsx3's native format)
            wav_path = output_path.replace('.mp3', '.wav')
            
            self.logger.info("Generating audio...")
            self.engine.save_to_file(text, wav_path)
            self.engine.runAndWait()
            
            # Check if file was created
            if os.path.exists(wav_path):
                self.logger.info(f"Audio saved to: {wav_path}")
                
                # If user requested MP3 but we have WAV, just return the WAV path
                # In a real app, you'd convert it, but we're keeping it simple
                return wav_path
            else:
                raise Exception("Audio file was not created")
                
        except Exception as e:
            self.logger.error(f"TTS conversion failed: {str(e)}")
            raise Exception(f"Text-to-speech conversion failed: {str(e)}")
    
    def set_voice_properties(self, rate: int = None, volume: float = None):
        """Adjust voice properties"""
        if rate is not None:
            self.engine.setProperty('rate', rate)
        if volume is not None:
            self.engine.setProperty('volume', volume)
    
    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'engine'):
            self.engine.stop()