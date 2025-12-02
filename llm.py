# llm.py
# Handles the text enrichment (rewriting) in English

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# --- THIS IS THE FIX ---
# We are using a stable, active free model.
# If this ever fails, try: "mistralai/mistral-7b-instruct:free"
MODEL_NAME = "google/gemini-2.0-flash-exp:free"

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
    Rewrites the text in English to make it a better script.
    """
    client = get_client()
    if not client: return None

    system_prompt = """
    You are a professional audiobook scriptwriter.
    Rewrite the provided text to be engaging, clear, and easy to listen to.
    Keep it in English. Do not translate it yet.
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Text to rewrite:\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"LLM Error: {e}")
        return None