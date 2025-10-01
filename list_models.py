# list_models.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# 2. Configurar o cliente LLM com a sua chave de API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Chave de API não encontrada. Verifique seu arquivo .env")
else:
    genai.configure(api_key=api_key)

    # 3. Listar os modelos e imprimir informações úteis
    print("--- Modelos Disponíveis ---")
    for model in genai.list_models():
        # Para o nosso caso, só nos interessam modelos que suportam 'generateContent'
        if 'generateContent' in model.supported_generation_methods:
            print(f"Nome para API: {model.name}")
            print(f"Métodos Suportados: {model.supported_generation_methods}")
            print(f"Descrição: {model.description}\n")
            print("---------------------------")