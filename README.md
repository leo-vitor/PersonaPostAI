# 🤖 PersonaPost AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](URL_DA_SUA_APP_STREAMLIT_AQUI)

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-red?style=for-the-badge&logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue?style=for-the-badge&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

Um gerador de conteúdo para redes sociais potencializado pela API do Google Gemini, projetado para criar posts personalizados com base em personas, objetivos e temas específicos, com persistência de dados por navegador.

---

### 🚀 **Acesse a Aplicação Ao Vivo:** [COLE A URL DA SUA APP STREAMLIT AQUI](COLE_A_URL_DA_SUA_APP_STREAMLIT_AQUI)

## 🎥 Demonstração

> **Nota:** É altamente recomendável que você grave um GIF da sua aplicação funcionando e o coloque aqui. Ferramentas como **ScreenToGif** ou **Kap** são ótimas para isso. Depois, basta fazer o upload do GIF para o repositório e substituir o link abaixo.

![Demonstração do PersonaPost AI](URL_DO_SEU_GIF_AQUI.gif)

## 🎯 Sobre o Projeto

O PersonaPost AI foi criado para resolver um desafio comum de criadores de conteúdo: a dificuldade de criar posts que sejam consistentes com a voz de uma marca e, ao mesmo tempo, criativos e alinhados a objetivos de marketing.

Esta aplicação web full-stack utiliza o poder da IA generativa do Google Gemini para criar, em segundos, múltiplas opções de posts para diferentes plataformas, tudo a partir de uma interface simples e intuitiva, "lembrando" das personas de cada usuário entre as visitas.

## ✨ Funcionalidades Principais

* **Persistência de Dados por Navegador:** Utiliza `localStorage` para salvar as personas de um usuário, garantindo que elas estejam disponíveis em visitas futuras sem a necessidade de login.
* **Gerenciamento de Personas:** Crie e salve personas detalhadas, que ficam disponíveis em um menu de seleção para uso rápido.
* **Sugestão de Temas com IA:** Se estiver sem ideias, a aplicação pode sugerir tópicos de posts relevantes para a persona selecionada.
* **Adaptação Multi-plataforma:** Gere conteúdo otimizado para Instagram, LinkedIn e Twitter/X.
* **Formatação Automática:** A resposta da IA é automaticamente analisada e formatada em abas, com sugestões de mídia e hashtags destacadas.
* **Interface Limpa e Reativa:** Construído com Streamlit, utilizando uma barra lateral fixa para uma experiência de usuário fluida.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Back-end:** FastAPI, Uvicorn
* **Front-end:** Streamlit, Streamlit Local Storage
* **IA Generativa:** Google Gemini API
* **Banco de Dados:** PostgreSQL (Produção), SQLite (Desenvolvimento), SQLAlchemy (ORM)
* **Comunicação API:** Requests, Pydantic
* **Deploy:** Render (Back-end + BD), Streamlit Community Cloud (Front-end)

## 🏛️ Arquitetura

O projeto utiliza uma arquitetura de cliente-servidor desacoplada, o que o torna flexível e escalável. Essa separação permite que a lógica de IA possa ser reutilizada por qualquer outro cliente no futuro (como um aplicativo mobile) sem nenhuma alteração no back-end.

```
[Usuário] <--> [🎈 Streamlit Cloud] <--> [🚀 Render Web Service] <--> [🧠 Google Gemini API]
                                             ^
                                             |
                                             v
                                          [🐘 PostgreSQL no Render]
```

## 🚀 Como Rodar Localmente

Siga os passos abaixo para executar o projeto na sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/leo-vitor/PersonaPostAI.git](https://github.com/leo-vitor/PersonaPostAI.git)
    cd PersonaPostAI
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv_personapost
    source venv_personapost/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas credenciais:**
    * Crie um arquivo `.env` e adicione sua chave da API do Google Gemini:
        ```
        GEMINI_API_KEY="SUA_CHAVE_DE_API_AQUI"
        ```

5.  **Execute a aplicação:**
    * **Terminal 1 (Back-end):**
        ```bash
        uvicorn api:app --reload
        ```
    * **Terminal 2 (Front-end):**
        ```bash
        streamlit run app.py
        ```

6.  Acesse `http://localhost:8501`.

## 📄 Licença

Este projeto está sob a licença MIT.

---

Feito com ❤️ por **Léo Vitor**.

[<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/leo-vitor/)
[<img src="https://img.shields.io/badge/github-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white" />](https://github.com/leo-vitor)