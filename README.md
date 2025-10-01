# 🤖 PersonaPost AI

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

Um gerador de conteúdo para redes sociais potencializado pela API do Google Gemini, projetado para criar posts personalizados com base em personas, objetivos e temas específicos.

---

## 🎯 Sobre o Projeto

O PersonaPost AI foi criado para resolver um desafio comum de criadores de conteúdo e gestores de redes sociais: a dificuldade de criar posts que sejam consistentes com a voz de uma marca e, ao mesmo tempo, criativos e alinhados a objetivos de marketing.

Esta aplicação web utiliza o poder da IA generativa do Google Gemini para criar, em segundos, múltiplas opções de posts para diferentes plataformas, tudo a partir de uma interface simples e intuitiva.

## ✨ Funcionalidades Principais

* **Geração Baseada em Persona:** Crie uma persona detalhada com nome, descrição e tom de voz para garantir que o conteúdo gerado seja perfeitamente alinhado com a sua marca.
* **Conteúdo Orientado a Objetivos:** Selecione um objetivo de marketing (Educar, Engajar, Vender, etc.) para que a IA foque o post na direção certa.
* **Adaptação Multi-plataforma:** Gere conteúdo otimizado para Instagram, LinkedIn e Twitter/X com um único clique.
* **Opções Criativas:** A aplicação sempre retorna duas opções distintas para cada post, oferecendo mais alternativas para o criador de conteúdo.
* **Interface Limpa e Reativa:** Construído com Streamlit para uma experiência de usuário fluida e agradável.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes tecnologias:

* **Linguagem:** Python 3.11+
* **Back-end:** FastAPI, Uvicorn
* **Front-end:** Streamlit
* **IA Generativa:** Google Gemini API (`gemini-pro-latest`)
* **Comunicação API:** Requests, Pydantic
* **Gerenciamento de Ambiente:** python-dotenv, Ambientes Virtuais (venv)

## 🏛️ Arquitetura

O projeto utiliza uma arquitetura de cliente-servidor desacoplada, o que o torna flexível e escalável.

* O **Front-end**, construído com **Streamlit**, é responsável exclusivamente pela interface do usuário. Ele coleta os dados e os exibe de forma amigável.
* O **Back-end**, construído com **FastAPI**, expõe uma API RESTful. Ele recebe as requisições do front-end, valida os dados, processa a lógica de negócios (chamando a API do Gemini) e retorna uma resposta estruturada em JSON.

Essa separação permite que a lógica de IA possa ser reutilizada por qualquer outro cliente no futuro (como um aplicativo mobile ou um chatbot) sem nenhuma alteração no back-end.

```
[Usuário] <--> [🎈 Streamlit Front-end] <--> [🚀 FastAPI Back-end] <--> [🧠 Google Gemini API]
```

## 🚀 Como Rodar Localmente

Siga os passos abaixo para executar o projeto na sua máquina.

**Pré-requisitos:**
* Python 3.9+
* Git

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/leo-vitor/PersonaPostAI.git](https://github.com/leo-vitor/PersonaPostAI.git)
    cd PersonaPostAI
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Crie o ambiente
    python -m venv venv_personapost

    # Ative o ambiente (Linux/macOS)
    source venv_personapost/bin/activate
    # ou (Windows)
    # venv_personapost\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas credenciais:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Dentro dele, adicione sua chave da API do Google Gemini:
        ```
        GEMINI_API_KEY="SUA_CHAVE_DE_API_AQUI"
        ```

5.  **Execute a aplicação:**
    * Você precisará de **dois terminais** abertos na pasta do projeto (com o ambiente virtual ativado em ambos).

    * **No Terminal 1**, inicie o servidor do back-end:
        ```bash
        uvicorn api:app --reload
        ```

    * **No Terminal 2**, inicie o servidor do front-end:
        ```bash
        streamlit run app.py
        ```

6.  Abra seu navegador e acesse `http://localhost:8501`.

## 📈 Próximos Passos

Este projeto tem um grande potencial para expansão. Os próximos passos planejados incluem:

* [ ] **Gerenciamento de Personas:** Implementar um banco de dados (SQLite) para salvar, carregar e deletar personas.
* [ ] **Sugestão de Temas:** Adicionar uma funcionalidade para que a IA sugira temas de posts com base na persona.
* [ ] **Histórico de Gerações:** Salvar os últimos posts gerados para fácil acesso.
* [ ] **Deploy:** Publicar a aplicação em uma plataforma de nuvem (Streamlit Community Cloud para o front-end, Render para o back-end).

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

Feito com ❤️ por **Léo Vitor**.

[<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/leo-vitor/)
[<img src="https://img.shields.io/badge/github-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white" />](https://github.com/leo-vitor)
