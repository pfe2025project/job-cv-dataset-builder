# 🧠 Annotation Automatique - Matching CV / Offre

## 📝 Introduction

Ce module est dédié à l'**annotation automatique** d'un dataset à partir d’un ensemble d'offres d’emploi et de CVs classés par domaine.  
L'objectif est de préparer les données nécessaires pour entraîner un modèle de **matching intelligent** entre les offres et les profils de candidats.

---

## 🎯 Objectif de l'annotation

Pour **chaque offre d’emploi**, un ensemble de **100 CVs** sera assigné, réparti selon la similarité de leur domaine par rapport à celui de l’offre :

- 50 CVs du **même domaine** que l’offre
- 25 à 30 CVs de **domaines similaires**
- 20 à 25 CVs de **domaines éloignés**

Cette organisation permet d’introduire de la diversité et de simuler un scénario réaliste pour la détection automatique de bons et mauvais matchs.

---

## 🔍 Démarche de sélection


### 1. 🔎 Collecte et identification du domaine des offres

Les offres sont collectées et stockées par domaine dans le dossier suivant :  
`scraping/offers/`

Exemple :  
`scraping/offers/data_science/offer1.txt` → domaine = `data_science`

> 🗒️ **Note** :  
> Si vous souhaitez consulter le processus complet de récupération et d'organisation des offres, veuillez vous référer au fichier [`job_scraper/docs.md`](job_scraper/docs.md).

---

### 2. 📁 Organisation et classification des CVs

Les CVs sont également organisés et stockés par domaine dans le dossier suivant :  
`scraping/cvs/{domaine}/cvX.txt`

Exemple :  
`scraping/cvs/data_science/cv1.txt` → domaine = `data_science`

> 🗒️ **Note** :  
> Si vous souhaitez consulter le processus complet de récupération et d'organisation des CVs, veuillez vous référer au fichier [`cv_scraper/docs.md`](cv_scraper/docs.md).

---


### 3. 🎯 Constitution du jeu de N CVs par offre (100 cvs par exemple)
Pour chaque offre, les CVs sont sélectionnés et répartis selon les critères suivants (les pourcentages et le nombre de CVs dans l'exemple sont à titre indicatif, et la répartition exacte est gérée dans le notebook) :

| Type de domaine     | Pourcentage approx. | Nombre de CVs | Source                              |
|---------------------|----------------------|----------------|--------------------------------------|
| 🟢 Même domaine     | 50%                  | ~50            | Même dossier que l’offre             |
| 🟡 Domaines proches | 25-30%               | ~25-30         | Dossiers manuellement définis        |
| 🔴 Domaines lointains| 20-25%              | ~20-25         | Dossiers différents / éloignés       |

Les CVs sont assignés **aléatoirement** depuis ces dossiers pour garantir de la variabilité.

Par exemple, pour chaque offre, un total de **N CVs** sera sélectionné, répartis entre les trois types de domaines mentionnés ci-dessus. Le nombre exact de CVs par offre est spécifié par le paramètre `cvs_per_offer` dans le script.

La fonction de préparation des CVs pour l'annotation est gérée par la fonction `prepare_to_annotate` qui est stockée dans `utils/utils.py`. 

Elle est appelée dans le notebook de la manière suivante :

```python
# Appel de la fonction avec chemins relatifs corrects
prepare_to_annotate(
    offers_path="../scraping/offres",
    cvs_path="../scraping/cvs",
    domain_map=domain_map,
    output_path="ready_to_annotate.csv",
    cvs_per_offer=5
)
```
---
## 📝 Processus d'annotation

Une fois les CVs sélectionnés pour chaque offre, le processus d'annotation commence. L'annotation consiste à évaluer la correspondance entre l'offre d'emploi et les CVs sélectionnés. Pour chaque CV, un score entre **0** et **1** est attribué, représentant la pertinence du CV par rapport à l'offre d'emploi.

### 🎯 Attribution du score / niveau

Ce score permettra de mesurer la correspondance sémantique entre l'offre et le CV, où un score plus proche de **1** indique une forte pertinence, et un score proche de **0** indique une faible pertinence.



---
## 🤖 Évaluation automatique via LLM

Pour automatiser l’annotation, nous avons testé plusieurs modèles, dont **DeepSeek** accessible via la plateforme OpenRouter, **Ollama**, et **Groq**.

1. **DeepSeek via OpenRouter** : Ce modèle joue le rôle d’un expert RH virtuel et attribue un score de pertinence entre 0 et 1 à chaque couple offre/CV, sur la base de leur compatibilité sémantique. Cependant, l'appel à l'API de DeepSeek via OpenRouter s'est révélé relativement lent, ce qui a rendu son utilisation moins optimale pour un grand nombre d'annotations.

2. **Ollama** : Bien qu’il ait montré de bons résultats en termes de précision, Ollama a également montré des performances de traitement plus lentes, rendant l'annotation de grandes quantités de données difficile.

3. **Groq** : Après avoir testé plusieurs solutions, nous avons choisi **Groq** comme outil principal pour l'évaluation des scores, car il a montré une meilleure réactivité et efficacité pour traiter rapidement les offres et les CVs.

Le processus d'annotation est géré par la fonction `annotate_data` dans le fichier [annotate_data.ipynb](annotate_data.ipynb). Cette fonction :

- Effectue la lecture des fichiers CV et offres.
- Génère les prompts et envoie les requêtes au modèle (Groq dans notre cas).
- Enregistre les scores obtenus dans un fichier `annotated_data.csv`.

### Exemple de génération de prompt

Voici comment le prompt est généré pour envoyer au modèle :

```python
def generate_prompt(offer_text, cv_text):
    return f"""
Tu es un expert en recrutement. Évalue la pertinence de ce CV pour cette offre d’emploi.

### Offre :
{offer_text}

### CV :
{cv_text}

Donne uniquement un score de similarité entre 0 et 1 (float), sans aucune explication ni commentaire.
Réponds uniquement par le nombre.
"""

---

```



## 📦 Résultat

les scores obtenus sont sauvegardés dans le fichier suivant :
[`data/labled_data.csv`](../data/labled_data.csv)

---