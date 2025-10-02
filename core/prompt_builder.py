# core/prompt_builder.py

from . import prompt_templates

def build_prompt(persona: dict, objetivo: str, tema: str, redes_sociais: list[str]) -> str:
    """Constrói o prompt final dinamicamente."""
    
    prompt = prompt_templates.PROMPT_TEMPLATE

    #Substitui os blocos das redes sociais selecionadas
    if "instagram" in redes_sociais:
        prompt = prompt.replace("{bloco_instagram}", prompt_templates.INSTAGRAM_BLOCK)
    
    if "linkedin" in redes_sociais:
        prompt = prompt.replace("{bloco_linkedin}", prompt_templates.LINKEDIN_BLOCK)
        
    if "twitter_x" in redes_sociais:
        prompt = prompt.replace("{bloco_twitter_x}", prompt_templates.TWITTER_X_BLOCK)
    
    #Remove os blocos das redes sociais não selecionadas
    prompt = prompt.replace("{bloco_instagram}", "")
    prompt = prompt.replace("{bloco_linkedin}", "")
    prompt = prompt.replace("{bloco_twitter_x}", "")

  
    final_prompt = prompt.format(
        nome_da_persona=persona.get('nome', ''),
        descricao_da_persona=persona.get('descricao', ''),
        tom_de_voz=persona.get('tom_de_voz', ''),
        objetivo=objetivo,
        tema=tema
    )
        
    return final_prompt