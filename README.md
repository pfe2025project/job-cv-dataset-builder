# 🧰 job-cv-dataset-builder

> 📦 Repo de collecte, annotation et préparation de données pour le matching entre CVs et offres d'emploi.

---

## 🎯 Objectif

Ce dépôt a pour but de :
- Collecter des **offres d’emploi** via scraping ou datasets publics
- Extraire et convertir des **CVs** (formats PDF / Word → texte brut)
- Annoter automatiquement les paires offre/CV avec des **labels (entre 0 et 1)** en utilisant des **LLM** (GPT, Gemini…)
- Nettoyer, prétraiter et structurer les données pour l'entraînement d’un modèle de **matching NLP**

---

## 📂 Structure des données

Les **CVs** et les **offres d’emploi** collectés sont stockés dans les dossiers **`scraping/cvs/`** et **`scraping/offers/`**, organisés par domaine (ex. frontend/, backend/, data_science/, etc.).

L’annotation automatique (labellisation) est gérée par un script situé dans le dossier **`annotation/`**.

Le dataset final labellisé est sauvegardé dans **`data/labled_data.csv`**, prêt pour l'entraînement d'un modèle NLP.

---

## 🛠️ Préparation du dataset

Le script lit les chemins des offres et des CVs, extrait le texte brut, associe le score de similarité et enregistre tout dans **`data/labled_data.csv`** sous la forme :

| offer_text | cv_text | score |
|:----------:|:-------:|:-----:|

Ce fichier est directement prêt pour un usage en **fine-tuning**, **entraînement supervisé** ou **évaluation de matching modèle**.

---

## 🚀 Guides

### Génération de CVs

📄 Guide ➔ [cv_scraper/docs.md](./cv_scraper/docs.md)

---

### Génération d'Offres

📄 Guide ➔ [job_scraper/docs.md](./job_scraper/docs.md)

---

### Annotation

📄 Guide ➔ [annotation/docs.md](./annotation/docs.md)


---