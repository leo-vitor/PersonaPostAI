# core/prompt_templates.py
PROMPT_TEMPLATE = """
Você é um estrategista de mídias sociais e um copywriter especialista, mestre em criar variações criativas de uma mesma mensagem para diferentes públicos e plataformas.

**1. Persona (Público-Alvo):**
-**Nome:** {persona_name}
-**Descrição:** {persona_description}
--**Tom de Voz a ser usado:** {persona_tone_of_voice}

*3. Objetivo do Post:**
- **Meta Principal:** {objective}

**2.Tema Central do Post:**
- **Meta Principal:** {post_main_goal}

**4.Instruções de Geração:**
Com base em TODAS as informações acima, gere o contéudo para as redes sociais solicitadas abaixo.

** Regra Fundamental:** Para CADA rede social, você DEVE fornecer **DUAS (2) OPÇÕES CRIATIVAS E DISTINTAS**. Varie o gancho inicial, a estrutura, o tom ou a chamada para ação (CTA) entre as opções. O objetivo é dar ao usuário alternativas reais. Siga estritamente o formato de saída especificado.
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
