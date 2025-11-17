import os
from openai import OpenAI
import google.generativeai as genai

def enrich_text_with_llm(text: str, provider: str, api_key: str) -> str:
    """
    Enrich text using LLM to make it more suitable for audiobook narration.
    
    Args:
        text: The raw extracted text
        provider: LLM provider ("OpenAI (GPT-3.5)", "OpenAI (GPT-4)", "Google Gemini")
        api_key: API key for the selected provider
    
    Returns:
        Enriched text suitable for audiobook narration
    """
    
    # Prompt for text enrichment
    prompt = f"""You are an expert audiobook narrator and editor. Your task is to rewrite the following text 
to make it more engaging and suitable for audiobook narration.

Guidelines:
1. Make the text flow naturally when read aloud
2. Add appropriate pauses and emphasis where needed
3. Fix any grammatical issues or awkward phrasing
4. Keep the original meaning and content intact
5. Make it engaging and pleasant to listen to
6. If the text is very technical, add brief clarifications where helpful

Original Text:
{text}

Rewritten Text for Audiobook:"""
    
    try:
        if "OpenAI" in provider:
            # Use OpenAI API
            client = OpenAI(api_key=api_key)
            
            model = "gpt-3.5-turbo" if "GPT-3.5" in provider else "gpt-4"
            
            # Split text into chunks if it's too long (max 4000 tokens ~16000 chars)
            max_chunk_size = 12000
            if len(text) > max_chunk_size:
                chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
                enriched_chunks = []
                
                for chunk in chunks:
                    chunk_prompt = prompt.replace(text, chunk)
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are an expert audiobook narrator and editor."},
                            {"role": "user", "content": chunk_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=2000
                    )
                    enriched_chunks.append(response.choices[0].message.content)
                
                return " ".join(enriched_chunks)
            else:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an expert audiobook narrator and editor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
        
        elif "Gemini" in provider:
            # Use Google Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash-')
            
            # Split text into chunks if it's too long
            max_chunk_size = 12000
            if len(text) > max_chunk_size:
                chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
                enriched_chunks = []
                
                for chunk in chunks:
                    chunk_prompt = prompt.replace(text, chunk)
                    response = model.generate_content(chunk_prompt)
                    enriched_chunks.append(response.text)
                
                return " ".join(enriched_chunks)
            else:
                response = model.generate_content(prompt)
                return response.text
        
        else:
            # If provider not recognized, return original text
            return text
    
    except Exception as e:
        raise Exception(f"Error enriching text with {provider}: {str(e)}")