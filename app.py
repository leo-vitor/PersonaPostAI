# app.py

import streamlit as st
import requests
import json

# URL da API back-end FastAPI
API_URL = "http://127.0.0.1:8000/generate"

#---- Configuração da página do Streamlit ----  
st.set_page_config(
    page_title="PersonaPostAI",
    page_icon="🤖",
    layout="wide")

st.title("🤖 PersonaPostAI")
st.markdown("Gere conteúdos para redes sociais baseados em personas.")


# ---- Layout com duas colunas ----
col1, col2 = st.columns([1, 1])

# ---- Coluna da Esquerda: Formulário de Entrada ----
with col1:
    st.header("Defina sua Persona")
    persona_name = st.text_input("Nome da Persona", placeholder="Ex: Clínica Odontológica, Pet Shop, Loja de Roupas")
    persona_description = st.text_area("Descrição da Persona", placeholder="Ex: Clínica localizada em Fortaleza-CE, deseja um conteúdo jovem e irreverente.")
    tone_of_voice = st.selectbox("Tom de Voz", options=["Formal", "Informal", "Inspirador e motivacional", "Divertido e leve", "Profissional e técnico"])

    st.header("Detalhes do Contéudo")
    objective = st.text_input("Objetivo do Post", placeholder="Ex: Aumentar o engajamento nas redes sociais")
    post_main_goal = st.text_input("Tema Central do Post", placeholder="Ex: Uso de aparelhos ortodônticos, Cuidados com pets no verão, Tendências de moda para 2024")

    redes_sociais = st.multiselect(
        "Selecione as Redes Sociais",
        options=["instagram", "linkedin", "twitter_x"],
        default=["instagram"]
    )
    
    submit_button = st.button("Gerar Posts ✨", type="primary", use_container_width=True)

# ---- Coluna da Direita: Resultados ----    
with col2:
    st.header("Conteúdo Gerado")
   
    if submit_button:
        if not all([persona_name, persona_description, tone_of_voice, objective, post_main_goal, redes_sociais]):
            st.error("Por favor, preencha todos os campos do formulário.")
        else:
            with st.spinner("Gerando conteúdo... Isso pode levar alguns segundos."):
                persona_dict = {
                    'name': persona_name,
                    'description': persona_description,
                    'tone_of_voice': tone_of_voice
                }
                request_data = {
                    "persona": persona_dict,
                    "objetivo": objective,
                    "tema": post_main_goal,
                    "redes_sociais": redes_sociais
                }
                
                try:
                    response = requests.post(API_URL, json=request_data, timeout=60)

                    if response.status_code == 200:
                        result = response.json()
                        if "content" in result:
                            st.markdown(result["content"])
                        else:
                            st.error(f"Erro na geração de conteúdo: {result.get('error', 'Erro desconhecido.')}")
                    else:
                        st.error(f"Erro na API: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Erro de conexão. Verifique se a API está em execução.")
                except Exception as e:
                    st.error(f"Ocorreu um erro inesperado: {e}") 
