# core/llm_client.py
import os
import google.generativeai as genai

def configure_llm():
    """Configura a API do Gemini com a chave fornecida."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave de API do Gemini não encontrada. Defina a variável de ambiente GEMINI_API_KEY no arquivo .env.")
    genai.configure(api_key=api_key)

def generate_content(prompt: str) -> str:
    """Gera conteúdo usando o modelo Gemini."""
    model = genai.GenerativeModel('gemini-pro-latest')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao gerar conteúdo: {e}")
        return None