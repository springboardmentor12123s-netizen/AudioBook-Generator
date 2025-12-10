import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

MODEL_LIST = [
    "meta-llama/llama-3-8b-instruct:free",      
    "google/gemini-2.0-flash-exp:free",         
    "qwen/qwen-2-7b-instruct:free",             
    "mistralai/mistral-7b-instruct:free"        
]

def configure_openrouter():
    load_dotenv()
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            st.error("🚨 OPENROUTER_API_KEY not found in .env file.")
            return False
        return True
    except Exception as e:
        st.error(f"Error configuring OpenRouter: {e}")
        return False

def get_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

def enrich_text_in_english(text):
    """
    Rewrites the text in English. Tries multiple models if one fails.
    """
    client = get_client()
    if not client: return None

    system_prompt = "You are a professional audiobook scriptwriter. Rewrite the provided text to be engaging, clear, and easy to listen to. Keep it in English."
    
    for model_name in MODEL_LIST:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Text to rewrite:\n{text}"}
                ]
            )
            content = response.choices[0].message.content
            
            if content and content.strip() != "":
                return content 
            
        except Exception as e:
            continue
            
    st.error("All free AI models are currently busy or unavailable. Please try again in 1 minute.")
    return None
