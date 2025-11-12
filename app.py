# app.py

import streamlit as st
import requests
import json
import time
import uuid
from streamlit_local_storage import LocalStorage

# --- Configuração da Página ---
st.set_page_config(page_title="PersonaPost AI", page_icon="🤖", layout="wide")

# --- URLs da API ---
# Lê a URL dos "secrets" no deploy, ou usa a URL local para desenvolvimento
try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", "http://127.0.0.1:8000")
except FileNotFoundError:
    API_BASE_URL = "http://127.0.0.1:8000"

GENERATE_URL = f"{API_BASE_URL}/generate"
PERSONAS_URL = f"{API_BASE_URL}/personas/"
SUGGEST_URL = f"{API_BASE_URL}/suggest-topics"

# --- Lógica de Persistência com LocalStorage ---
localS = LocalStorage()

def get_persistent_session_id():
    """
    Busca o session_id do localStorage.
    Se não existir, cria um novo, salva e o retorna.
    """
    session_id = localS.getItem("session_id")
    if not session_id:
        new_id = str(uuid.uuid4())
        localS.setItem("session_id", new_id)
        return new_id
    return session_id

session_id = get_persistent_session_id()
        
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

def get_personas(sid):
    """Busca as personas associadas ao session_id atual."""
    if not sid: return []
    try:
        response = requests.get(f"{PERSONAS_URL}{sid}", timeout=600)
        if response.status_code == 200:
            return response.json()
        return []
    # Captura genérica para qualquer erro de requisição (Timeout, Conexão, etc.)
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Erro ao carregar personas. O servidor pode estar 'acordando'. Tente recarregar a página.")
        print(f"Erro em get_personas: {e}")
        return None

def create_persona(sid, nome, descricao, tom_de_voz):
    """Cria uma nova persona enviando o session_id junto."""
    persona_data = {
        "nome": nome,
        "descricao": descricao,
        "tom_de_voz": tom_de_voz,
        "session_id": sid
    }
    # Timeout aumentado para 120s
    return requests.post(PERSONAS_URL, json=persona_data, timeout=600)

#---- Título  ----  
st.title("🤖 PersonaPost AI")
st.markdown("### Gere conteúdos para redes sociais baseados em personas.")

# ---- BARRA LATERAL (CONTROLES) ----
with st.sidebar:
    st.header("1. Selecione ou Crie uma Persona")
    
   
    personas_list = get_personas(session_id)
    persona_options = {}
    selected_persona_name = ""

    if personas_list is not None:
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
                    current_session_id = session_id
                    if not current_session_id:
                        current_session_id = str(uuid.uuid4())
                        localS.setItem("session_id", current_session_id)
                        time.sleep(0.5) 
                    
                    response = create_persona(current_session_id, new_name, new_description, new_tone)
                    
                    if response.status_code == 200:
                        st.success(f"Persona '{new_name}' criada!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        error_message = f"Erro ao criar persona. Status: {response.status_code}."
                        try:
                            details = response.json().get('detail')
                            if details: error_message += f" Detalhe: {details}"
                        except json.JSONDecodeError:
                            error_message += f" Resposta do servidor: {response.text}"
                        st.error(error_message)
                else:
                    st.error("Preencha todos os campos.")
                
    st.header("2. Defina o Conteúdo")
    objetivo = st.text_input("Objetivo do Post", placeholder="Ex: Aumentar o engajamento")

    if st.button("💡 Sugerir Temas"):
        if selected_persona_name:
            with st.spinner("Buscando inspiração..."):
                selected_persona_details = persona_options[selected_persona_name]
                try:
                    response = requests.post(SUGGEST_URL, json={"persona": selected_persona_details}, timeout=600)
                    if response.status_code == 200:
                        result = response.json()
                        if "topics" in result and result["topics"]:
                            st.session_state.suggested_topics = result["topics"]
                            st.session_state.generation_history = []
                            st.rerun()
                        else:
                            st.warning("A IA não retornou sugestões.")
                    else:
                        st.error("Erro ao obter sugestões da API.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de API ao sugerir temas: {e}")
        else:
            st.warning("Selecione uma persona para obter sugestões.")

    tema = st.text_input("Tema Central do Post", placeholder="Ex: Copie uma sugestão ou digite um tema")
    redes_sociais = st.multiselect(
        "Selecione as Redes Sociais",
        options=["instagram", "linkedin", "twitter_x"],
        default=["instagram"]
    )
    
    submit_button = st.button("Gerar Posts ✨", type="primary", use_container_width=True)

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
                response = requests.post(GENERATE_URL, json=request_data, timeout=600)
                if response.status_code == 200:
                    result = response.json()
                    if "content" in result:
                        st.session_state.suggested_topics = []
                        st.session_state.generation_history.insert(0, result["content"])
                        st.session_state.generation_history = st.session_state.generation_history[:5]
                        st.rerun()
                    else:
                        st.error(f"Erro da API: {result.get('error', 'Erro desconhecido')}")
                else:
                    st.error(f"Erro na API: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro de API ao gerar post: {e}")

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