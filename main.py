import os
from dotenv import load_dotenv
from core.llm_client import configure_llm, generate_content
from core.prompt_builder import build_prompt

def run_test():
    """ Função principal para roda rum teste completo. """
    #1. Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()
    # 2. Configura o cliente LLM com a chave da API
    try:
        configure_llm()
    except ValueError as ve:
        print(ve)
        return
    #3. Simula as entradas do usuário
    mock_persona = {
        'name': 'Clinica Odontologica' ,
        'description': 'Clinica Odontologica localizada em Fortaleza-CE, deseja um conteudo jovem e irreverente.',
        'tone_of_voice': 'Inspirador e motivacional'
    }
    mock_objetivo = 'Aumentar o engajamento nas redes sociais'
    mock_tema = 'Uso de aparelhos ortodônticos'
    mock_redes_sociais = ['instagram', 'twitter_x']

    print("-----Iniciando Geração de Conteúdo-----")
    print(f"Persona: {mock_persona}")
    print(f"Objetivo: {mock_objetivo}")
    print(f"Tema: {mock_tema}")
    print(f"Redes Sociais: {mock_redes_sociais}")
    print("---------------------------------------")

    #4. Constrói o prompt completo
    prompt = build_prompt(mock_persona, mock_objetivo, mock_tema, mock_redes_sociais)
    print("Prompt Construído:")

    #5. Gera o conteúdo usando o LLM
    print("Aguardando resposta do modelo de IA... Isso pode levar alguns segundos.")
    response = generate_content(prompt)

    #6. Exibe o resultado
    if response:
        print("Conteúdo Gerado com Sucesso:")
        print(response)
    else:
        print("Falha ao gerar conteúdo.")

if __name__ == "__main__":
    run_test()        
    
