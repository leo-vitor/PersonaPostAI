# api.py

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from contextlib import asynccontextmanager 
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Importa a nossa lógica e os modulos de banco de dados
from core import models
from core import prompt_templates
from core.database import SessionLocal, create_db_and_tables 
from core.llm_client import configure_llm, generate_content
from core.prompt_builder import build_prompt

load_dotenv()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Criando o banco de dados e as tabelas, se não existirem...")
    create_db_and_tables()
    print("Iniciando a aplicação e configurando o LLM...")
    configure_llm()
    yield
    print("Aplicação encerrada.")

app = FastAPI(
    lifespan=lifespan,
    title="PersonaPost AI API",
    description="API para gerar posts de redes sociais baseados em personas.",
    version="1.1.0"
)

# --- CORREÇÃO FINAL AQUI ---
# Padronizando os modelos Pydantic para português
class PersonaBase(BaseModel):
    nome: str
    descricao: str
    tom_de_voz: str

class PersonaCreate(PersonaBase):
    pass

class Persona(PersonaBase):
    id: int
    class Config:
        # 'orm_mode' foi renomeado para 'from_attributes' no Pydantic V2
        from_attributes = True

class PostRequest(BaseModel):
    persona: dict
    objetivo: str
    tema: str
    redes_sociais: List[str] 
class SuggestedTopicsRequest(BaseModel):
    persona: dict


@app.post("/personas/", response_model=Persona)
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db)):
    db_persona = models.Persona(**persona.model_dump())
    try:
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
        return db_persona
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Uma persona com o nome '{persona.nome}' já existe.")
    
@app.get("/personas/", response_model=List[Persona])
def read_personas(db:Session = Depends(get_db)):
    personas = db.query(models.Persona).all()
    return personas 

# api.py

# ... (resto do arquivo, sem alterações) ...

@app.post("/suggest-topics") 
def suggest_topics_endpoint(request: SuggestedTopicsRequest):
    try:
        prompt = prompt_templates.SUGGEST_TOPICS_PROMPT_TEMPLATE.format(
            nome_da_persona=request.persona.get('nome', ''),
            descricao_da_persona=request.persona.get('descricao', '')
        )
        raw_response = generate_content(prompt)

        print(f"DEBUG: Resposta crua da IA para sugestões: {raw_response}")

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

# 
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
        # Retorna o erro como string para ajudar na depuração
        return {"error": f"Ocorreu um erro inesperado no servidor: {e}"}