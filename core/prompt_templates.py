# core/prompt_templates.py

PROMPT_TEMPLATE = """
Você é um gerador de conteúdo para redes sociais. Sua tarefa é criar posts com base nas informações fornecidas, seguindo as regras de formatação de forma precisa.

**1. Persona (Público-Alvo):**
- **Nome:** {nome_da_persona}
- **Descrição:** {descricao_da_persona}
- **Tom de Voz a ser usado:** {tom_de_voz}

**2. Objetivo do Post:**
- **Meta Principal:** {objetivo}

**3. Tema Central do Post:**
- **Assunto:** {tema}

**4. Instruções de Geração:**
Com base em TODAS as informações acima, gere o conteúdo para as seções de redes sociais solicitadas abaixo. Para cada seção, forneça **DUAS (2) OPÇÕES CRIATIVAS E DISTINTAS**.

---
**REGRAS ESTRITAS DE SAÍDA:**
- NÃO inclua saudações, introduções, despedidas, resumos de estratégia ou qualquer texto que não seja o próprio conteúdo do post formatado.
- NÃO escreva "Opção 1", "Opção 2", "Legenda", "Tweet", etc. Siga exatamente a estrutura dos blocos de formatação.
- Sua resposta deve começar DIRETAMENTE com a primeira linha da primeira seção solicitada (ex: `**[SAÍDA PARA INSTAGRAM]**`).
---
{bloco_instagram}
---
{bloco_linkedin}
---
{bloco_twitter_x}
"""

INSTAGRAM_BLOCK = """
**[SAÍDA PARA INSTAGRAM]**
**[OPÇÃO 1]**
- **Legenda:** [Escreva aqui a primeira versão da legenda]
- **Sugestão de Mídia:** [Descreva a sugestão de mídia para a opção 1]
- **Hashtags:** [Sugira 5 hashtags para a opção 1]
**[OPÇÃO 2]**
- **Legenda:** [Escreva aqui a segunda versão da legenda, com uma abordagem diferente]
- **Sugestão de Mídia:** [Descreva uma sugestão de mídia alternativa para a opção 2]
- **Hashtags:** [Sugira 5 hashtags diferentes ou com uma nova combinação para a opção 2]
"""

LINKEDIN_BLOCK = """
**[SAÍDA PARA LINKEDIN]**
**[OPÇÃO 1]**
- **Texto do Post:** [Escreva aqui a primeira versão do texto para LinkedIn]
- **Hashtags:** [Sugira 3 hashtags profissionais para a opção 1]
**[OPÇÃO 2]**
- **Texto do Post:** [Escreva aqui a segunda versão do texto, com abordagem diferente]
- **Hashtags:** [Sugira 3 hashtags profissionais diferentes para a opção 2]
"""

TWITTER_X_BLOCK = """
**[SAÍDA PARA TWITTER/X]**
**[OPÇÃO 1]**
- **Tweet:** [Escreva aqui a primeira versão do tweet, concisa e impactante]
- **Hashtags:** [Sugira 2 hashtags relevantes para a opção 1]
**[OPÇÃO 2]**
- **Tweet:** [Escreva aqui a segunda versão do tweet, com um gancho diferente]
- **Hashtags:** [Sugira 2 hashtags relevantes diferentes para a opção 2]
"""

SUGGEST_TOPICS_PROMPT_TEMPLATE = """
Você é um estrategista de conteúdo especialista em brainstorming. Sua tarefa é gerar ideias de posts para redes sociais com base em uma persona.

**Persona:**
- **Nome:** {nome_da_persona}
- **Descrição:** {descricao_da_persona}

Com base na persona acima, gere 5 ideias de temas para posts. Os temas devem ser curtos, diretos e interessantes para o público-alvo descrito.

**REGRAS ESTRITAS DE SAÍDA:**
- Retorne a resposta como uma lista numerada, e NADA MAIS.
- NÃO inclua saudações, introduções, despedidas ou qualquer texto adicional.

Exemplo de Saída:
1. Tema A
2. Tema B
3. Tema C

"""