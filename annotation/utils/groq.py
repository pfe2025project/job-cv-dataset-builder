import requests
import os
import time
import random
import json
import re
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY2")

# def generate_prompt(offer_text, cv_text):
#     return f"""
# Tu es un expert en recrutement. Évalue la pertinence de ce CV pour cette offre d’emploi.

# ### Offre :
# {offer_text}

# ### CV :
# {cv_text}

# Donne uniquement un score de similarité entre 0 et 1 (sous forme de nombre flottant). 
# ⚠️ Ne donne rien d'autre que ce nombre. Pas d'explication, pas de justification. Juste le score.
# """


def generate_prompt(offer_text, cv_text):
    return f"""
Tu es un expert en recrutement. Évalue la pertinence de ce CV pour cette offre d’emploi.

### Offre :
{offer_text}

### CV :
{cv_text}

Voici comment évaluer :
- Si le CV correspond parfaitement au poste → score proche de 1.0.
- Si le CV est du même domaine mais pas parfaitement adapté → score entre 0.5 et 0.8.
- Si le CV est partiellement relié mais loin des compétences demandées → score entre 0.3 et 0.5.
- Si le CV n’a presque aucun lien → score < 0.3.

Donne uniquement un score de similarité entre 0 et 1 (sous forme de nombre flottant).
⚠️ Ne donne rien d'autre que ce nombre. Pas d'explication, pas de justification. Juste le score.
"""

def get_groq_score(offer_text, cv_text):
    prompt = generate_prompt(offer_text, cv_text)

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("Error:", response.status_code, response.text)
        return "error"


# Fonction de récupération du score avec gestion des erreurs 429 pour Groq
def get_groq_score_with_retry(offer_text, cv_text, retries=10):
    for attempt in range(retries):
        try:
            result = get_groq_score(offer_text, cv_text)
            if isinstance(result, str) and 'error' in result.lower():
                raise Exception("Received error from API.")
            return safe_extract_score(result) if not is_float(result) else float(result)
        except Exception as e:
            if "Rate limit reached" in str(e):  # Vérifie si l'erreur est liée au rate limit 429
                print(f"⏳ Erreur 429 : Attente avant réessai...")
                print(f"🕒 Temps d'attente avant réessai : 18 secondes")
                time.sleep(30)  # Attendre 18 secondes avant de réessayer
            elif "Received error from API" in str(e):  # Vérifie si l'erreur est liée au rate limit 429
                print(f"⏳ Erreur 429 : Attente avant réessai...")
                print(f"🕒 Temps d'attente avant réessai : 18 secondes")
                time.sleep(30)  # Attendre 18 secondes avant de réessayer
            else:
                raise e
    raise Exception("Échec après plusieurs tentatives.")






# Fonction pour vérifier si c'est un float valide
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Fonction pour extraire un score d'un texte (exemple: "Similarité : 0.2")
def safe_extract_score(text):
    match = re.search(r"(\d+\.\d+)", text)
    if match:
        return float(match.group(1))
    else:
        raise ValueError(f"Aucun score valide trouvé dans : {text}")