# app.py

import streamlit as st
import requests
import json
import time
import uuid
import os
from streamlit_local_storage import LocalStorage
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

# --- Importações Diretas da Lógica de Back-end ---
# (Assumindo que todos os arquivos core/*.py estão corretos)
from core.database import SessionLocal, create_db_and_tables, get_db
from core.models import Persona
from core.llm_client import configure_llm, generate_content
from core.prompt_builder import build_prompt
from core import prompt_templates

# --- Configuração da Página (deve ser o primeiro comando st) ---
st.set_page_config(page_title="PersonaPost AI", page_icon="🤖", layout="wide")

# --- Configurar Banco de Dados e API de IA (Executa apenas uma vez) ---
@st.cache_resource
def init_connections():
    """Cria tabelas do BD e configura a API do Gemini uma vez."""
    print("Iniciando: Criando tabelas do BD...")
    create_db_and_tables()
    
    print("Iniciando: Configurando API do Gemini...")
    try:
        # Tenta carregar do Streamlit Secrets (Produção)
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            raise FileNotFoundError # Força a ida para o except local
        configure_llm(GEMINI_API_KEY)
        print("API do Gemini configurada via st.secrets.")
    except (FileNotFoundError, AttributeError):
        # Se falhar (local), carrega do .env
        print("st.secrets não encontrado. Carregando do .env local...")
        load_dotenv()
        configure_llm() # llm_client lerá do os.getenv()
        print("API do Gemini configurada via .env.")

init_connections()

# --- URLs da API (Apenas para referência futura, não mais usadas) ---
# API_BASE_URL = ... (removido)

# --- Lógica de Persistência com LocalStorage ---
localS = LocalStorage()
session_id = localS.getItem("session_id")
if not session_id:
    session_id = str(uuid.uuid4())
    localS.setItem("session_id", session_id)
        
# --- Estado da Sessão para UI (Histórico e Sugestões) ---
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []
if 'suggested_topics' not in st.session_state:
    st.session_state.suggested_topics = []

# --- Funções ---
def parse_ai_response(text: str) -> dict:
    """Analisa a resposta de texto da IA e a estrutura em um dicionário."""
    parsed_data = {}
    plataformas = text.split('[SAÍDA PARA ')
    for plataforma_bloco in plataformas:
        if ']' not in plataforma_bloco:
            continue
        nome_plataforma, conteudo = plataforma_bloco.split(']', 1)
        nome_plataforma = nome_plataforma.strip()
        opcoes = []
        blocos_opcao = conteudo.split('[OPÇÃO ')
        for i, bloco_opcao in enumerate(blocos_opcao):
            if i == 0: continue
            opcao_data = {}
            if "Legenda:" in bloco_opcao:
                opcao_data['legenda'] = bloco_opcao.split("Legenda:", 1)[1].split("Sugestão de Mídia:", 1)[0].strip()
            elif "Tweet:" in bloco_opcao:
                 opcao_data['legenda'] = bloco_opcao.split("Tweet:", 1)[1].split("Hashtags:", 1)[0].strip()
            elif "Texto do Post:" in bloco_opcao:
                 opcao_data['legenda'] = bloco_opcao.split("Texto do Post:", 1)[1].split("Hashtags:", 1)[0].strip()
            if "Sugestão de Mídia:" in bloco_opcao:
                opcao_data['sugestao'] = bloco_opcao.split("Sugestão de Mídia:", 1)[1].split("Hashtags:", 1)[0].strip()
            if "Hashtags:" in bloco_opcao:
                opcao_data['hashtags'] = bloco_opcao.split("Hashtags:", 1)[1].strip()
            opcoes.append(opcao_data)
        parsed_data[nome_plataforma] = opcoes
    return parsed_data

# --- NOVAS Funções de Lógica (Conexão Direta com BD) ---
def get_personas_from_db(sid: str, db: Session):
    """Busca as personas direto do banco de dados."""
    if not sid: return []
    try:
        personas = db.query(Persona).filter(Persona.session_id == sid).all()
        # Converte objetos SQLAlchemy para dicts
        return [{"id": p.id, "nome": p.nome, "descricao": p.descricao, "tom_de_voz": p.tom_de_voz, "session_id": p.session_id} for p in personas]
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar personas: {e}")
        return []

def create_persona_in_db(sid: str, nome: str, descricao: str, tom_de_voz: str, db: Session):
    """Cria uma nova persona direto no banco de dados."""
    persona_data = Persona(
        nome=nome,
        descricao=descricao,
        tom_de_voz=tom_de_voz,
        session_id=sid
    )
    try:
        db.add(persona_data)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        st.error(f"Erro: Uma persona com o nome '{nome}' já existe.")
        return False
    except Exception as e:
        db.rollback()
        st.error(f"Erro ao salvar persona: {e}")
        return False

#---- Título ----  
st.title("🤖 PersonaPost AI")
st.markdown("### Gere conteúdos para redes sociais baseados em personas.")

# ---- BARRA LATERAL (CONTROLES) ----
with st.sidebar:
    st.header("1. Selecione ou Crie uma Persona")
    
    # Obtém uma sessão de banco de dados para usar na barra lateral
    db = next(get_db())
    
    personas_list = get_personas_from_db(session_id, db)
    persona_options = {}
    selected_persona_name = ""

    if personas_list:
        persona_options = {p['nome']: p for p in personas_list}
        nomes_das_personas = list(persona_options.keys())
        selected_persona_name = st.selectbox(
            "Personas Salvas",
            options=[""] + nomes_das_personas,
            format_func=lambda x: "Selecione uma persona" if x == "" else x
        )
    else:
        st.info("Nenhuma persona salva. Crie uma nova abaixo.")

    with st.expander("➕ Criar Nova Persona"):
        with st.form("new_persona_form", clear_on_submit=True):
            new_name = st.text_input("Nome da Persona")
            new_description = st.text_area("Descrição da Persona")
            new_tone = st.text_area("Tom de Voz")
            submitted = st.form_submit_button("Salvar Persona")
            if submitted:
                if new_name and new_description and new_tone:
                    success = create_persona_in_db(session_id, new_name, new_description, new_tone, db)
                    if success:
                        st.success(f"Persona '{new_name}' criada!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("Preencha todos os campos.")
                
    st.header("2. Defina o Conteúdo")
    objetivo = st.text_input("Objetivo do Post", placeholder="Ex: Aumentar o engajamento")

    if st.button("💡 Sugerir Temas"):
        if selected_persona_name:
            with st.spinner("Buscando inspiração..."):
                selected_persona_details = persona_options[selected_persona_name]
                try:
                    # Chama a lógica de IA diretamente
                    prompt = prompt_templates.SUGGEST_TOPICS_PROMPT_TEMPLATE.format(
                        nome_da_persona=selected_persona_details.get('nome'),
                        descricao_da_persona=selected_persona_details.get('descricao')
                    )
                    raw_response = generate_content(prompt)
                    if raw_response:
                        topics = [line.split('. ', 1)[1] for line in raw_response.strip().split('\n') if '. ' in line]
                        st.session_state.suggested_topics = topics
                        st.session_state.generation_history = []
                        st.rerun()
                    else:
                        st.warning("A IA não retornou sugestões.")
                except Exception as e:
                    st.error(f"Erro ao sugerir temas: {e}")
        else:
            st.warning("Selecione uma persona para obter sugestões.")

    tema = st.text_input("Tema Central do Post", placeholder="Ex: Copie uma sugestão ou digite um tema")
    redes_sociais = st.multiselect(
        "Selecione as Redes Sociais",
        options=["instagram", "linkedin", "twitter_x"],
        default=["instagram"]
    )
    
    submit_button = st.button("Gerar Posts ✨", type="primary", use_container_width=True)
    
    db.close() # Fecha a sessão do banco de dados no final da renderização da sidebar

# ---- PÁGINA PRINCIPAL (RESULTADOS) ----
st.header("🚀 Posts Gerados")

if st.session_state.suggested_topics:
    st.info("Aqui estão algumas sugestões! Copie e cole uma no campo 'Tema Central' ao lado.")
    topics_markdown = "- " + "\n- ".join(st.session_state.suggested_topics)
    st.markdown(topics_markdown)
    st.markdown("---")

if submit_button:
    if not selected_persona_name:
        st.error("Por favor, selecione uma persona na lista.")
    elif not tema or not redes_sociais:
        st.error("Por favor, preencha o tema e selecione ao menos uma rede social.")
    else:
        with st.spinner("Gerando conteúdo... 🧠"):
            selected_persona_details = persona_options[selected_persona_name]
            request_data = {
                "persona": selected_persona_details,
                "objetivo": objetivo,
                "tema": tema,
                "redes_sociais": redes_sociais
            }
            try:
                # Chama a lógica de IA diretamente
                final_prompt = build_prompt(request_data["persona"], request_data["objetivo"], request_data["tema"], request_data["redes_sociais"])
                raw_response = generate_content(final_prompt)
                
                if raw_response:
                    st.session_state.suggested_topics = []
                    st.session_state.generation_history.insert(0, raw_response)
                    st.session_state.generation_history = st.session_state.generation_history[:5]
                    st.rerun()
                else:
                    st.error(f"Erro da API: A IA não retornou conteúdo.")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")

if st.session_state.generation_history:
    st.markdown("### Resultado Mais Recente")
    latest_result = st.session_state.generation_history[0]
    parsed_content = parse_ai_response(latest_result)
    for plataforma, opcoes in parsed_content.items():
        st.subheader(f"📱 {plataforma.title()}")
        if len(opcoes) >= 2:
            tab1, tab2 = st.tabs(["Opção 1", "Opção 2"])
            with tab1:
                st.markdown(opcoes[0].get('legenda', ''))
                if 'sugestao' in opcoes[0]:
                    with st.expander("🎨 Ver Sugestão de Mídia"):
                        st.write(opcoes[0]['sugestao'])
                if 'hashtags' in opcoes[0]:
                    st.code(opcoes[0]['hashtags'], language='bash')
            with tab2:
                st.markdown(opcoes[1].get('legenda', ''))
                if 'sugestao' in opcoes[1]:
                    with st.expander("🎨 Ver Sugestão de Mídia"):
                        st.write(opcoes[1]['sugestao'])
                if 'hashtags' in opcoes[1]:
                    st.code(opcoes[1]['hashtags'], language='bash')
    
    if len(st.session_state.generation_history) > 1:
        st.markdown("---")
        st.markdown("### Histórico de Gerações Anteriores")
        for i, old_content in enumerate(st.session_state.generation_history[1:]):
            with st.expander(f"📜 Histórico {i+1}"):
                parsed_old_content = parse_ai_response(old_content)
                for plataforma, opcoes in parsed_old_content.items():
                    st.subheader(f"📱 {plataforma.title()}")
                    if len(opcoes) >= 2:
                        tab1, tab2 = st.tabs([f"Opção 1", f"Opção 2"])
                        with tab1:
                            st.markdown(opcoes[0].get('legenda', ''))
                        with tab2:
                            st.markdown(opcoes[1].get('legenda', ''))