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

    n_same = int(n_total * 0.4)
    n_similar = int(n_total * 0.3)
    n_diff = n_total - n_same - n_similar

    # Pools
    same_pool = cvs_by_domain.get(domain, [])
    similar_domains = get_similar_domains(domain, domain_map)
    similar_pool = [cv for d in similar_domains for cv in cvs_by_domain.get(d, [])]
    all_domains = set(cvs_by_domain.keys())
    different_domains = list(all_domains - set(similar_domains) - {domain})
    different_pool = [cv for d in different_domains for cv in cvs_by_domain.get(d, [])]

    # Actual selections
    same_selected = random.sample(same_pool, min(n_same, len(same_pool)))
    similar_selected = random.sample(similar_pool, min(n_similar, len(similar_pool)))
    different_selected = random.sample(different_pool, min(n_diff, len(different_pool)))

    # Count how many more we need
    total_selected = len(same_selected) + len(similar_selected) + len(different_selected)
    remaining = n_total - total_selected

    # Refill from any available pool to reach n_total
    remaining_pool = list(set(same_pool + similar_pool + different_pool) - 
                          set(same_selected + similar_selected + different_selected))
    if remaining > 0:
        extra_selected = random.sample(remaining_pool, min(remaining, len(remaining_pool)))
    else:
        extra_selected = []

    # Combine everything
    result = [(cv, 'same') for cv in same_selected] + \
             [(cv, 'similar') for cv in similar_selected] + \
             [(cv, 'different') for cv in different_selected] + \
             [(cv, 'extra') for cv in extra_selected]

    # 🪵 Print the summary
    print(f"🔎 CV selection summary for domain '{domain}': "
          f"{len(same_selected)} same, {len(similar_selected)} similar, "
          f"{len(different_selected)} different, {len(extra_selected)} extra → Total: {len(result)}")

    return result




def prepare_to_annotate(offers_path, cvs_path, domain_map, output_path,cvs_per_offer=5):
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

        offer_count = 0
        for root, dirs, files in os.walk(offers_path):
            for file in files:
                if file.endswith('.txt') or file.endswith('.pdf'):
                    offer_path = os.path.join(root, file)
                    domain = os.path.basename(os.path.dirname(offer_path))
                    selected_cvs = select_cvs_for_offer(domain, cvs_by_domain, domain_map,n_total=cvs_per_offer)

                    for cv_path, _ in selected_cvs:
                        writer.writerow([offer_path, cv_path])

                    offer_count += 1
                    print(f"📌 {len(selected_cvs)} CVs added for offer {offer_count} located at path: {offer_path}")
                else:
                    print(f"⚠️ Fichier ignoré (ni .txt ni .pdf) : {file}")




