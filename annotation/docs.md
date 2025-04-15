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

### 1. 🔎 Identification du domaine de l'offre
Le domaine est inféré à partir du dossier contenant l’offre.  
Exemple : `scraping/offers/data_science/offer1.txt` → domaine = `data_science`

### 2. 📁 Organisation des CVs
Les CVs sont déjà stockés par domaine dans :  
`scraping/cvs/{domaine}/cvX.txt`

### 3. 🎯 Constitution du jeu de 100 CVs
Pour chaque offre :

| Type de domaine     | Pourcentage approx. | Nombre de CVs | Source                              |
|---------------------|----------------------|----------------|--------------------------------------|
| 🟢 Même domaine     | 50%                  | ~50            | Même dossier que l’offre             |
| 🟡 Domaines proches | 25-30%               | ~25-30         | Dossiers manuellement définis        |
| 🔴 Domaines lointains| 20-25%              | ~20-25         | Dossiers différents / éloignés       |

Les CVs sont assignés **aléatoirement** depuis ces dossiers pour garantir de la variabilité.

## 📝 Processus d'annotation

Une fois les CVs sélectionnés pour chaque offre, le processus d'annotation commence. L'annotation consiste à évaluer la correspondance entre l'offre d'emploi et les CVs sélectionnés. Pour chaque CV, un score ou un niveau est attribué, représentant la pertinence du CV par rapport à l'offre d'emploi.

### 🎯 Attribution du score / niveau

- **Score élevé** : Le CV est fortement pertinent pour l'offre d'emploi.
- **Score moyen** : Le CV est partiellement pertinent, mais manque de certaines compétences clés.
- **Score faible** : Le CV est peu pertinent pour l'offre, avec peu de correspondance en termes de compétences ou d'expérience.

Cette évaluation sera utilisée pour entraîner un modèle de matching automatique capable de classer les CVs en fonction de leur pertinence pour une offre d'emploi donnée.



---

## 🧰 Scripts

Les scripts liés à cette tâche seront disponibles dans le dossier :


annotation/
├── assign_cv_to_offers.py
├── utils.py
└── ...


---