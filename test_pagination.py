
import time
import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://books.toscrape.com/"
nombre_pages = 0

# Liste commune à toutes les pages
livres_recuperes = []
erreur_reseau = False
while url is not None and nombre_pages < 2:

    
    try:
        reponse = requests.get(url, timeout=10)
        reponse.raise_for_status()
        reponse.encoding = "utf-8"
    except requests.exceptions.RequestException as erreur:
        erreur_reseau = True
        print("Erreur pendant la récupération :", erreur)
        break


    soup = BeautifulSoup(reponse.text, "html.parser")

    livres = soup.select("article.product_pod")

    nombre_pages += 1

    print(f"PAGE {nombre_pages}")

    for livre in livres:

        lien = livre.select_one("h3 a")
        prix_element = livre.select_one(".price_color")

        if lien is None or prix_element is None:
            continue

        titre = lien.get("title")
        prix_texte = prix_element.get_text(strip=True)

        prix = float(prix_texte.replace("£", "").strip())

        href = lien.get("href")

        if not href:
            continue

        url_livre = urljoin(reponse.url, href)

        livre_dict = {
            "titre": titre,
            "prix": prix,
            "url": url_livre
        }

        livres_recuperes.append(livre_dict)

    suivant = soup.select_one("li.next a")

    if suivant is not None and suivant.get("href"):
        url = urljoin(reponse.url, suivant.get("href"))
    else:
        url = None

    if url is not None and nombre_pages < 2:
        time.sleep(1)

print("\nScraping terminé !")
if erreur_reseau:
    print("Collecte interrompue : résultats incomplets")
else:
    print("Collecte terminée sans erreur réseau")

print("Nombre de livres récupérés :", len(livres_recuperes))


# Sauvegarder seulement si aucune erreur réseau n'a interrompu la collecte
if not erreur_reseau:

    # Créer le dossier data s'il n'existe pas
    dossier = Path("data")
    dossier.mkdir(exist_ok=True)

    # Définir le chemin du fichier
    chemin = dossier / "livres.json"

    # Écrire les données dans le fichier
    with open(chemin, "w", encoding="utf-8") as fichier:
        json.dump(livres_recuperes, fichier, ensure_ascii=False, indent=4)

    print("Données enregistrées dans :", chemin)

with open("data/livres.json", "r", encoding="utf-8") as fichier:
    livres = json.load(fichier)
print("Nombre de livres dans le fichier :", len(livres))
print("Exemple de livre :", livres[0]["titre"],",",livres[0]["prix"] if livres else "Aucun livre trouvé")