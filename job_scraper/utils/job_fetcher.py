import requests
import os
import re
import json
from utils.job_desc_scraper import scrape_full_description
from fpdf import FPDF  # Assure-toi d'avoir installé: pip install fpdf
from dotenv import load_dotenv
load_dotenv()

# --- Identifiants Adzuna ---
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_API_KEY")
COUNTRY = "us"
RESULTS_PER_KEYWORD = 3  # 👈 Tu veux seulement 3 résultats par mot-clé

# Charger la structure des domaines depuis un fichier JSON
def load_domains(path):
    with open(path, 'r') as file:
        return json.load(file)

# Fonction pour récupérer les offres d'emploi en fonction des mots-clés
def fetch_jobs_by_keyword(keyword, max_results=RESULTS_PER_KEYWORD):
    url = (
        f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
        f"?app_id={APP_ID}&app_key={APP_KEY}"
        f"&results_per_page={max_results}&what={keyword}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"❌ Erreur API {response.status_code} pour '{keyword}'")
        return []

def sanitize_filename(filename):
    # Remplacer les /, \ et autres caractères spéciaux par _
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

# Sauvegarder chaque offre d'emploi dans un fichier TXT ou PDF
def save_jobs_to_file(domain, keyword, jobs, base_path, format='txt'):
    domain_path = os.path.join(base_path, sanitize_filename(domain))
    os.makedirs(domain_path, exist_ok=True)

    for idx, job in enumerate(jobs, 1):
        title = job.get('title', 'No Title')
        company = job.get('company', {}).get('display_name', 'Unknown Company')
        location = job.get('location', {}).get('display_name', 'Unknown Location')
        link = job.get('redirect_url', '')
        
        print(f"       🔄 scrape desc for: {link} ...")
        try:
            description = scrape_full_description(link)
        except Exception as e:
            print(f"       ⚠️ Erreur lors du scraping de l'offre: {e}. Lien ignoré.")
            continue  # Skip this job and move to the next

        content = f"""Title: {title}
        Company: {company}
        Location: {location}
        
        Description:
        {description}
        """

        # Utilisation du mot-clé pour le nom de fichier
        sanitized_keyword = sanitize_filename(keyword)
        file_basename = f"{sanitized_keyword}_job_{idx}"

        if format == 'txt':
            file_path = os.path.join(domain_path, f"{file_basename}.txt")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde du fichier TXT pour '{file_basename}': {e}")

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
                print(f"❌ Erreur lors de la sauvegarde du fichier PDF pour '{file_basename}': {e}")

# Fonction principale
def fetch_and_save_jobs_for_domain(domain_structure, base_path, max_results=1, format='txt'):
    print("🚀 Démarrage de la collecte des offres...\n")
    total_domains = len(domain_structure)
    total_requests = 0  # Initialiser le compteur de requêtes

    for i, (domain, keywords) in enumerate(domain_structure.items(), 1):
        print(f"\n🔍 [{i}/{total_domains}] Domaine: {domain} - {len(keywords)} mot(s)-clé(s)")
        
        for j, keyword in enumerate(keywords, 1):
            print(f"   🔸 [{j}/{len(keywords)}] Recherche pour le mot-clé: '{keyword}'")
            
            jobs = fetch_jobs_by_keyword(keyword, max_results=max_results)
            nb_jobs = len(jobs)
            total_requests += 1  # Incrémenter le compteur de requêtes après chaque appel API
            
            if jobs:
                print(f"     ✅ {nb_jobs} offre(s) trouvée(s). Sauvegarde en cours...")
                save_jobs_to_file(domain, keyword, jobs, base_path, format=format)
                print(f"     📁 Offres enregistrées dans: {os.path.join(base_path, domain)}")
            else:
                print(f"     ⚠️ Aucune offre trouvée pour: {keyword}")
    
    print(f"\n✅ Terminé ! Toutes les offres ont été récupérées et sauvegardées.")
    print(f"🔢 Nombre total de requêtes exécutées: {total_requests}")  # Afficher le nombre total de requêtes exécutées
