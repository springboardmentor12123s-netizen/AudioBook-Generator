import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from .utils import chunk_text

# Load environment variables
load_dotenv()

class LLMEnrichment:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        
        # Use the available Gemini 2.5 Flash model
        self.model_name = "gemini-2.5-flash"
        self.model = genai.GenerativeModel(self.model_name)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using model: {self.model_name}")
    
    def enrich_text(self, text: str, chunk_size: int = 2000) -> str:
        """
        Rewrite text for engaging audiobook narration using Gemini
        """
        if len(text) <= chunk_size:
            return self._process_chunk(text)
        
        # Process in chunks for large texts
        chunks = chunk_text(text, chunk_size)
        enriched_chunks = []
        
        for i, chunk in enumerate(chunks):
            self.logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            enriched_chunk = self._process_chunk(chunk)
            enriched_chunks.append(enriched_chunk)
        
        return " ".join(enriched_chunks)
    
    def _process_chunk(self, text_chunk: str) -> str:
        """Process a single chunk of text"""
        prompt = f"""
        Rewrite the following text for an engaging audiobook narration. 
        Make it flow naturally when spoken aloud, with appropriate pacing and emphasis.
        Maintain the original meaning and key information.
        Use natural language that sounds good when read aloud.
        
        Text to rewrite:
        {text_chunk}
        
        Rewritten version:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            self.logger.error(f"Error in LLM processing: {str(e)}")
            # Return original text if processing fails
            return text_chunk