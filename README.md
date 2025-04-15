# 🧰 job-cv-dataset-builder

> 📦 repo de collecte, annotation et préparation de données pour le matching entre CVs et offres d'emploi.

---

## 🎯 Objectif

Ce dépôt a pour but de :
- Collecter des **offres d’emploi** via scraping ou datasets publics
- Extraire et convertir des **CVs** (formats PDF / Word → texte brut)
- Annoter automatiquement les paires offre/CV avec des **labels (0 ou 1)** en utilisant des **LLM** (GPT, Gemini…)
- Nettoyer, prétraiter et structurer les données pour l'entraînement d’un modèle de **matching NLP**

---

## 📂 Structure des données

Les **CVs** et les **offres d’emploi** collectés sont stockés dans les dossiers **scraping/cvs/** et **scraping/offers/**, organisés par domaine (ex. frontend/, backend/, data_science/, etc.).

L’annotation automatique (labellisation) est gérée par un script situé dans le dossier **annotation/**.

Le dataset final labellisé sera sauvegardé dans le dossier **data/**, prêt pour l'entraînement du modèle.

---
## Génération de CV

---
## Génération d'Offres

---
## Annotation

Guide ==> [annotation/docs.md](./annotation/docs.md)


---