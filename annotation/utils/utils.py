import os
import json
import random
import csv
from collections import defaultdict
from docx import Document
from PyPDF2 import PdfReader

def read_file_content(filepath):
    try:
        if filepath.endswith(".txt"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.read()

        elif filepath.endswith(".docx"):
            doc = Document(filepath)
            return '\n'.join([para.text for para in doc.paragraphs])

        elif filepath.endswith(".pdf"):
            text = ""
            with open(filepath, 'rb') as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ''
            return text

        else:
            print(f"⚠️ Format non supporté : {filepath}")
            return ""

    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {filepath}: {e}")
        return ""


def load_domain_map(path):
    with open(path, 'r') as f:
        return json.load(f)

def get_similar_domains(domain, domain_map):
    for group in domain_map.values():
        if domain in group:
            return [d for d in group if d != domain]
    return []

def get_cvs_by_domain(cvs_root):
    cvs_by_domain = defaultdict(list)
    for root, dirs, files in os.walk(cvs_root):
        for file in files:
            if file.endswith('.txt') or file.endswith('.pdf'):
                domain = os.path.basename(root)
                cvs_by_domain[domain].append(os.path.join(root, file))
    return cvs_by_domain

def select_cvs_for_offer(domain, cvs_by_domain, domain_map, n_total=100):
    result = []

    n_same = int(n_total * 0.5)
    n_similar = int(n_total * 0.3)
    n_diff = n_total - n_same - n_similar

    similar_domains = get_similar_domains(domain, domain_map)
    all_domains = set(cvs_by_domain.keys())
    different_domains = list(all_domains - set(similar_domains) - {domain})

    result += [(cv, 'same') for cv in random.sample(cvs_by_domain.get(domain, []), min(n_same, len(cvs_by_domain.get(domain, []))))]

    similar_pool = []
    for d in similar_domains:
        similar_pool += cvs_by_domain.get(d, [])
    result += [(cv, 'similar') for cv in random.sample(similar_pool, min(n_similar, len(similar_pool)))]

    different_pool = []
    for d in different_domains:
        different_pool += cvs_by_domain.get(d, [])
    result += [(cv, 'different') for cv in random.sample(different_pool, min(n_diff, len(different_pool)))]

    return result


def prepare_to_annotate(offers_path, cvs_path, domain_map, output_path):
    # Vérifier si les chemins existent
    if not os.path.exists(offers_path):
        raise FileNotFoundError(f"Le dossier des offres n'existe pas : {offers_path}")
    if not os.path.exists(cvs_path):
        raise FileNotFoundError(f"Le dossier des CVs n'existe pas : {cvs_path}")

    cvs_by_domain = get_cvs_by_domain(cvs_path)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['offer_path', 'cv_path'])
        print(f"📂 Analyse des offres dans : {offers_path}\n")

        for root, dirs, files in os.walk(offers_path):
            for file in files:
                if file.endswith('.txt') or file.endswith('.pdf'):
                    offer_path = os.path.join(root, file)
                    domain = os.path.basename(os.path.dirname(offer_path))
                    selected_cvs = select_cvs_for_offer(domain, cvs_by_domain, domain_map)

                    for cv_path, _ in selected_cvs:
                        print(f"✅ Offre : {offer_path}  |  CV : {cv_path}")
                        writer.writerow([offer_path, cv_path])
                else:
                    print(f"⚠️ Fichier ignoré (ni .txt ni .pdf) : {file}")



