import requests
import os
from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv("OPENROUTER_API_KEY")


def generate_prompt(offer_text, cv_text):
    return f"""
Tu es un expert en recrutement. Évalue la pertinence de ce CV pour cette offre d’emploi.

### Offre :
{offer_text}

### CV :
{cv_text}

Donne un score de similarité entre 0 et 1 (float). Ne donne que le score.
"""


def get_openrouter_score(offer_text, cv_text):
    prompt = generate_prompt(offer_text,cv_text)
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
    )
    score = response.json()["choices"][0]["message"]["content"]
    return score
