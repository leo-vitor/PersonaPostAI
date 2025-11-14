# core/database.py
import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from dotenv import load_dotenv

# Carrega variáveis do .env (para ambiente local)
load_dotenv()

# --- LÓGICA DE CONEXÃO CORRIGIDA ---

# 1. Tenta carregar do ambiente local (arquivo .env) primeiro.
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Se não achar (estiver na nuvem), tenta carregar do st.secrets.
if not DATABASE_URL:
    try:
        DATABASE_URL = st.secrets.get("DATABASE_URL")
    except (FileNotFoundError, AttributeError):
        DATABASE_URL = None # Continua como None se não achar em lugar nenhum

# 3. Se não houver URL (nem nuvem, nem .env), usa o SQLite local como padrão.
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./personapost.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # 4. Ajuste para a URL do PostgreSQL (Render/Produção)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)

# --- FIM DA CORREÇÃO ---

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """Cria as tabelas no banco de dados se elas não existirem."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Gerador de sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()