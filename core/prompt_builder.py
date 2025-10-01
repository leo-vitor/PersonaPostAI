from . import prompt_templates 

def build_prompt(persona: dict, objetivo: str, tema: str, redes_sociais: list[str]) -> str:
    """Constrói o prompt completo substituindo os placeholders no template."""   
    prompt = prompt_templates.PROMPT_TEMPLATE.format(
        persona_name=persona.get('name', 'N/A'),
        persona_description=persona.get('description', 'N/A'),
        persona_tone_of_voice=persona.get('tone_of_voice', 'N/A'),
        post_main_goal= tema,
        objective = objetivo,
        #Deixa os blcos vazios inicialmente
        bloco_instagram="",
        bloco_linkedin="",
        bloco_twitter_x=""
    )

    if 'instagram' in redes_sociais:
        prompt = prompt.replace("{bloco_instagram}", prompt_templates.INSTAGRAM_BLOCK)

    if 'linkedin' in redes_sociais:
        prompt = prompt.replace("{bloco_linkedin}", prompt_templates.LINKEDIN_BLOCK)    

    if 'twitter_x' in redes_sociais:
        prompt = prompt.replace("{bloco_twitter_x}", prompt_templates.TWITTER_X_BLOCK)    
    
    return prompt