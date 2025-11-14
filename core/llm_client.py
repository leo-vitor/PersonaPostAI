# core/llm_client.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

def configure_llm(api_key=None):
    """Configura a chave de API para o cliente Gemini."""
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Chave de API do Gemini não encontrada.")
    
    genai.configure(api_key=api_key)

def generate_content(full_prompt: str) -> str:
    """Chama a API do Gemini para gerar conteúdo."""
    model = genai.GenerativeModel('gemini-pro-latest') 
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API: {e}")
        return None