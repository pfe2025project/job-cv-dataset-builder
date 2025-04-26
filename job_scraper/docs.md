# Collecte et traitement des offres d'emploi
## 🎯 Objectif

L'objectif est de collecter automatiquement des offres d'emploi en ligne, de les organiser par domaines d'activité, et de compléter les descriptions lorsque celles-ci sont incomplètes, afin de constituer une base de données exploitable pour des analyses ultérieures.

---

### 🔎 Utilisation de l'API Adzuna

Pour collecter les offres d'emploi, nous avons utilisé l'**API Adzuna**, qui fournit un accès à de nombreuses annonces disponibles en ligne.  
Nous avons structuré et organisé les offres en fonction de plusieurs **domaines d'activité** afin de faciliter leur exploitation (ex : *Data Science*, *Développement*, etc.).

L'intégralité des scripts de collecte est disponible dans le **notebook**, avec des explications sur chaque étape.

Nous avons utilisé un script Python qui interroge l'API avec des paramètres spécifiques comme un **mot-clé** et une **langue**.

Voici un exemple simplifié d'appel API pour rechercher des offres contenant le mot-clé `"DATA SCIENCE DEVELOPER"` en langue française :

```python
# Exemple d'appel basique à l'API Adzuna
search_params = {
    "app_id": "YOUR_APP_ID",
    "app_key": "YOUR_APP_KEY",
    "what": "DATA SCIENCE DEVELOPER",
    "language": "fr",
    "results_per_page": 50
}
response = requests.get("https://api.adzuna.com/v1/api/jobs/fr/search/1", params=search_params)
jobs = response.json()
```
---


Le script de filtrage et de sauvegarde est disponible dans le notebook :  
[`fetch_jobs.ipynb`](fetch_jobs.ipynb)

## 📦 Résultat

Les CVs filtrés sont sauvegardés dans le répertoire suivant :
[`scraping/cvs/`](../scraping/offres/)
