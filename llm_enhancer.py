import os
from google import genai
from google.genai import types

# IMPORTANT: KEEP THIS COMMENT - using blueprint:python_gemini
# Note that the newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
# do not change this unless explicitly requested by the user

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# This API key is from Gemini Developer API Key, not vertex AI API Key
gemini_client = genai.Client(api_key=GEMINI_API_KEY)


def enhance_text_for_audiobook(text, chunk_size=3000):
    """
    Use Google Gemini's LLM to rewrite text in an engaging audiobook narration style.
    
    Args:
        text: The extracted text to enhance
        chunk_size: Maximum characters per chunk (to avoid token limits)
    
    Returns:
        Enhanced text suitable for audiobook narration
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("No text provided for enhancement")
    
    # Split text into manageable chunks if it's too long
    chunks = split_text_into_chunks(text, chunk_size)
    enhanced_chunks = []
    
    system_instruction = """You are an expert audiobook narrator and editor. Rewrite the following text to make it more engaging and suitable for audiobook narration. 

Guidelines:
- Make the text flow naturally when spoken aloud
- Add appropriate transitions between ideas
- Ensure smooth pacing for listening
- Keep the core content and meaning intact
- Make it engaging and pleasant to hear
- Remove any formatting artifacts or special characters that don't translate well to audio

Provide only the rewritten text, without any additional commentary."""
    
    for i, chunk in enumerate(chunks):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=chunk)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=1.0,
                )
            )
            
            enhanced_text = response.text
            if enhanced_text:
                enhanced_chunks.append(enhanced_text)
            else:
                raise ValueError("Empty response from Gemini")
            
        except Exception as e:
            raise Exception(f"Error enhancing text chunk {i+1}: {str(e)}")
    
    # Combine all enhanced chunks
    return "\n\n".join(enhanced_chunks)


def split_text_into_chunks(text, chunk_size=3000):
    """
    Split text into smaller chunks for processing.
    
    Args:
        text: The text to split
        chunk_size: Maximum characters per chunk
    
    Returns:
        List of text chunks
    """
    # If text is small enough, return as single chunk
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    paragraphs = text.split('\n')
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed chunk size
        if len(current_chunk) + len(paragraph) + 1 > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                # Single paragraph is too long, split it by sentences
                sentences = paragraph.split('. ')
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 2 > chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
                    else:
                        current_chunk += sentence + ". "
        else:
            current_chunk += paragraph + "\n"
    
    # Add the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

