import subprocess

def generate_prompt(offer_text, cv_text):
    return f"""
Tu es un expert en recrutement. Évalue la pertinence de ce CV pour cette offre d’emploi.

### Offre :
{offer_text}

### CV :
{cv_text}

Donne uniquement un score de similarité entre 0 et 1 (sous forme de nombre flottant). 
⚠️ Ne donne rien d'autre que ce nombre. Pas d'explication, pas de justification. Juste le score.
"""

def get_mistral_score(data):
    offer_text, cv_text = data
    prompt = generate_prompt(offer_text, cv_text)

    result = subprocess.run(
        ['ollama', 'run', 'mistral'],
        input=prompt,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    return result.stdout.strip()

