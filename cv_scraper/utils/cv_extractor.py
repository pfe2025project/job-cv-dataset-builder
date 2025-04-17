import os
import json
import pandas as pd
from fpdf import FPDF  # Assurez-vous d'avoir installé fpdf via pip
import re

# Charger la structure des domaines à partir du fichier JSON
def load_domains(path):
    with open(path, 'r') as file:
        return json.load(file)

# Fonction pour nettoyer les noms de fichiers (pour éviter les caractères spéciaux)
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

# Fonction pour sauvegarder les CV au format TXT ou PDF
def save_cv_to_file(domain, cv_texts, base_path, format='txt'):
    domain_path = os.path.join(base_path, sanitize_filename(domain))
    os.makedirs(domain_path, exist_ok=True)

    for idx, cv in enumerate(cv_texts, 1):
        file_basename = f"{sanitize_filename(domain)}_cv_{idx}"

        content = f"Résumé: {cv}"

        if format == 'txt':
            file_path = os.path.join(domain_path, f"{file_basename}.txt")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde du fichier TXT: {e}")

        elif format == 'pdf':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for line in content.split('\n'):
                pdf.multi_cell(0, 10, line)
            file_path = os.path.join(domain_path, f"{file_basename}.pdf")
            try:
                pdf.output(file_path)
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde du fichier PDF: {e}")

# Filtrer les CV par domaine et catégorie
def filter_cvs_by_domain_and_category(df, domain_structure,base_path):
    for domain, categories in domain_structure.items():
        # Filtrer le DataFrame pour obtenir les CV correspondant aux catégories du domaine
        domain_cvs = df[df['Category'].isin(categories)]['Resume'].tolist()
        
        # Sauvegarder ces CV dans un fichier pour ce domaine
        if domain_cvs:
            save_cv_to_file(domain, domain_cvs, base_path=base_path, format='txt')  # Utiliser format='pdf' si besoin
            print(f"✅ {len(domain_cvs)} CV(s) enregistrés pour le domaine: {domain}")
        else:
            print(f"⚠️ Aucun CV trouvé pour le domaine: {domain}")
