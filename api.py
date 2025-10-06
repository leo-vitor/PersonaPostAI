# api.py

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from contextlib import asynccontextmanager 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Importa a nossa lógica e os módulos de banco de dados
from core import models
from core import prompt_templates
from core.database import SessionLocal, create_db_and_tables 
from core.llm_client import configure_llm, generate_content
from core.prompt_builder import build_prompt

load_dotenv()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Gerenciador de eventos de inicialização e desligamento
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Criando o banco de dados e as tabelas, se não existirem...")
    create_db_and_tables()
    print("Iniciando a aplicação e configurando o LLM...")
    configure_llm()
    yield
    print("Aplicação encerrada.")

# Instância principal do FastAPI
app = FastAPI(
    lifespan=lifespan,
    title="PersonaPost AI API",
    description="API para gerar posts de redes sociais baseados em personas.",
    version="1.3.0" # Atualizamos a versão para refletir a lógica de sessão
)

# --- MODELOS PYDANTIC (Contratos da API) ---
class PersonaBase(BaseModel):
    nome: str
    descricao: str
    tom_de_voz: str

class PersonaCreate(PersonaBase):
    session_id: str 

class Persona(PersonaBase):
    id: int
    session_id: str
    class Config:
        from_attributes = True

class PostRequest(BaseModel):
    persona: dict
    objetivo: str
    tema: str
    redes_sociais: List[str] 

class SuggestTopicsRequest(BaseModel):
    persona: dict

# --- ENDPOINTS DA API ---

@app.post("/personas/", response_model=Persona)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    """Cria uma nova persona no banco de dados, associada a um session_id."""
    db_persona = models.Persona(**persona.model_dump())
    try:
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
        return db_persona
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao salvar a persona.")
    
@app.get("/personas/{session_id}", response_model=List[Persona])
def read_personas_by_session(session_id: str, db: Session = Depends(get_db)):
    """Lista apenas as personas que pertencem a um session_id específico."""
    personas = db.query(models.Persona).filter(models.Persona.session_id == session_id).all()
    return personas

@app.post("/suggest-topics") 
def suggest_topics_endpoint(request: SuggestTopicsRequest):
    """Gera sugestões de temas com base em uma persona."""
    try:
        prompt = prompt_templates.SUGGEST_TOPICS_PROMPT_TEMPLATE.format(
            nome_da_persona=request.persona.get('nome', ''),
            descricao_da_persona=request.persona.get('descricao', '')
        )
        raw_response = generate_content(prompt)
        if raw_response:
            topics = []
            for line in raw_response.strip().split('\n'):
                parts = line.split('. ', 1)
                if len(parts) == 2:
                    topics.append(parts[1].strip())
            return {"topics": topics}
        else:
            return {"error": "Falha ao gerar tópicos a partir do modelo de IA."}
    except Exception as e:
        return {"error": f"Ocorreu um erro inesperado no servidor: {e}"}    

@app.post("/generate")
def generate_post_endpoint(request: PostRequest):
    """Gera o conteúdo completo dos posts."""
    try:
        final_prompt = build_prompt(request.persona, request.objetivo, request.tema, request.redes_sociais)
        raw_response = generate_content(final_prompt)
        if raw_response:
            return {"content": raw_response}
        else:
            return {"error": "Falha ao gerar conteúdo a partir do modelo de IA."}
    except Exception as e:
        return {"error": f"Ocorreu um erro inesperado no servidor: {e}"}