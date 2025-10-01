# api.py

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from contextlib import asynccontextmanager 

# Importa a nossa lógica da Fase 1
from core.llm_client import configure_llm, generate_content
from core.prompt_builder import build_prompt

load_dotenv()

# FUNÇÃO "LIFESPAN"
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tudo que está ANTES do "yield" roda na inicialização (startup)
    print("Iniciando a aplicação e configurando o LLM...")
    configure_llm()
    
    yield
    
    # Tudo que está DEPOIS do "yield" roda no encerramento (shutdown)
    print("Aplicação encerrada.")

# REGISTRAR O "LIFESPAN" NA APLICAÇÃO
app = FastAPI(
    lifespan=lifespan,
    title="PersonaPost AI API",
    description="API para gerar posts de redes sociais baseados em personas.",
    version="1.0.0"
)


class PostRequest(BaseModel):
    persona: dict
    objetivo: str
    tema: str
    redes_sociais: List[str] = Field(..., min_length=1)

@app.post("/generate")
def generate_post_endpoint(request: PostRequest):
    try:
        final_prompt = build_prompt(request.persona, request.objetivo, request.tema, request.redes_sociais)
        raw_response = generate_content(final_prompt)
        
        if raw_response:
            return {"content": raw_response}
        else:
            return {"error": "Falha ao gerar conteúdo a partir do modelo de IA."}
    except Exception as e:
        return {"error": f"Ocorreu um erro inesperado no servidor: {e}"}