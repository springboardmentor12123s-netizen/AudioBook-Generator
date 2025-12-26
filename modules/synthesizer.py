"""
Text-to-Speech Module
Converts text to audio using ElevenLabs API
"""

from elevenlabs.client import ElevenLabs
import os


# Pre-defined voices from ElevenLabs
VOICES = {
    "21m00Tcm4TlvDq8ikWAM": {
        "name": "Rachel",
        "description": "Calm, young American female"
    },
    "29vD33N1CtxCmqQRPOHJ": {
        "name": "Drew",
        "description": "Well-rounded American male"
    },
    "2EiwWnXFnvU5JabPnv8n": {
        "name": "Clyde",
        "description": "War veteran, deep American male"
    },
    "5Q0t7uMcjvnagumLfvZi": {
        "name": "Paul",
        "description": "Ground reporter, American male"
    },
    "AZnzlk1XvdvUeBnXmlld": {
        "name": "Domi",
        "description": "Strong, young American female"
    },
    "EXAVITQu4vr4xnSDxMaL": {
        "name": "Sarah",
        "description": "Soft, young American female"
    },
    "ErXwobaYiN019PkySvjV": {
        "name": "Antoni",
        "description": "Well-rounded American male"
    },
    "MF3mGyEYCl7XYWbV9V6O": {
        "name": "Elli",
        "description": "Emotional, young American female"
    },
    "TxGEqnHWrfWFTfGW9XjX": {
        "name": "Josh",
        "description": "Deep, young American male"
    },
    "XB0fDUnXU5powFXDhCwa": {
        "name": "Charlotte",
        "description": "Seductive, Swedish female"
    },
    "Xb7hH8MSUJpSbSDYk0k2": {
        "name": "Alice",
        "description": "Confident, British female"
    },
    "XrExE9yKIg1WjnnlVkGX": {
        "name": "Matilda",
        "description": "Warm, young American female"
    },
    "pFZP5JQG7iQjIQuC4Bku": {
        "name": "Lily",
        "description": "Warm, British female"
    },
    "pNInz6obpgDQGcFmaJgB": {
        "name": "Adam",
        "description": "Deep, middle-aged American male"
    },
    "yoZ06aMxZJJ28mfd3POQ": {
        "name": "Sam",
        "description": "Raspy, young American male"
    },
    "onwK4e9ZLuTAKqWW03F9": {
        "name": "Daniel",
        "description": "Deep, authoritative British male"
    },
}


def get_available_voices():
    """
    Get list of available voices

    Returns:
        dict: Voice ID to voice info mapping
    """
    return VOICES


def text_to_speech(text, output_path, api_key, voice_id="EXAVITQu4vr4xnSDxMaL"):
    """
    Convert text to speech using ElevenLabs API and save as MP3

    Args:
        text: The text to convert to speech
        output_path: Path to save the audio file
        api_key: ElevenLabs API key
        voice_id: Voice ID to use (default: Sarah)

    Returns:
        dict: {"success": True, "path": "..."} or {"success": False, "error": "..."}
    """
    try:
        if not text:
            return {"success": False, "error": "No text provided for speech synthesis"}

        if not api_key:
            return {"success": False, "error": "ElevenLabs API key not configured"}

        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=api_key)

        # Generate audio
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        # Write audio to file
        with open(output_path, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)

        # Verify file was created
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return {"success": True, "path": output_path}
        else:
            return {"success": False, "error": "Failed to save audio file"}

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            return {"success": False, "error": "Invalid ElevenLabs API key"}
        elif "429" in error_msg:
            return {"success": False, "error": "API rate limit exceeded. Please try again later."}
        elif "insufficient" in error_msg.lower() or "quota" in error_msg.lower():
            return {"success": False, "error": "ElevenLabs quota exceeded. Please check your plan."}
        return {"success": False, "error": error_msg}
