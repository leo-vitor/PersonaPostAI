# app.py

import streamlit as st
import requests
import json
import time


# URLs da API back-end FastAPI
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://127.0.0.1:8000")
GENERATE_URL = f"{API_BASE_URL}/generate"
PERSONAS_URL = f"{API_BASE_URL}/personas/"
SUGGEST_URL = f"{API_BASE_URL}/suggest-topics"

if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []
if 'suggested_topics' not in st.session_state:
    st.session_state.suggested_topics = []

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

# ----- Funções de API (sem alterações) -----
def get_personas():
    try:
        response = requests.get(PERSONAS_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.ConnectionError:
        st.sidebar.error("API não conectada.") # Mover o erro para a sidebar
        return None

def create_persona(nome, descricao, tom_de_voz):
    persona_data = {
        "nome": nome,
        "descricao": descricao,
        "tom_de_voz": tom_de_voz
    }
    return requests.post(PERSONAS_URL, json=persona_data)

#---- Configuração da página do Streamlit ----  
st.set_page_config(page_title="PersonaPostAI", page_icon="🤖", layout="wide")

# ----BARRA LATERAL ----
with st.sidebar:
    st.title("🤖 PersonaPost AI")
    st.markdown("### Controles de Geração")
    
    st.header("Selecione ou Crie uma Persona")
    
    personas_list = get_personas()
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
                    response = create_persona(new_name, new_description, new_tone)
                    if response.status_code == 200:
                        st.success(f"Persona '{new_name}' criada!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Erro: {response.json().get('detail')}")
                else:
                    st.error("Preencha todos os campos.")
                
    st.header("Defina o Conteúdo")
    objetivo = st.text_input("Objetivo do Post", placeholder="Ex: Aumentar o engajamento")

    if st.button("Sugerir Tópicos(com base na Persona)"):
        if selected_persona_name:
            with st.spinner("Buscando Inspiração..."):
                selected_persona_details = persona_options[selected_persona_name]
                response = requests.post(SUGGEST_URL, json={"persona": selected_persona_details})
                if response.status_code == 200:
                    result = response.json()
                    if "topics" in result:
                        st.session_state.suggested_topics = result["topics"]
                        st.session_state.generation_history = []  # Limpa o histórico de geração ao sugerir novos tópicos
                        st.rerun()
                    else:
                        st.error("Erro ao obter tópicos sugeridos.")


    tema = st.text_input("Tema Central do Post")

    redes_sociais = st.multiselect(
        "Selecione as Redes Sociais",
        options=["instagram", "linkedin", "twitter_x"],
        default=["instagram"]
    )
    
    submit_button = st.button("Gerar Posts ✨", type="primary", use_container_width=True)

# ---- Resultados: PÁGINA PRINCIPAL ----
st.header("🚀 Posts Gerados")

if st.session_state.suggested_topics:
    st.info("Aqui estão algumas sugestões! Copie e cole uma no campo 'Tema Central' na barra lateral.")
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
                response = requests.post(GENERATE_URL, json=request_data)
                if response.status_code == 200:
                    result = response.json()
                    if "content" in result:
                        parsed_content = parse_ai_response(result["content"])
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
                            else:
                                st.warning(f"Não foi possível formatar as opções para {plataforma}.")
                    else:
                        st.error(f"Erro da API: {result.get('error', 'Erro desconhecido')}")
                else:
                    st.error(f"Erro na API: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")