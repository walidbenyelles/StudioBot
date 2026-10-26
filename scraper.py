
from bs4 import BeautifulSoup

def extraire_annonces():

    # Ouvrir le fichier HTML
    with open("annonces.html", "r", encoding="utf-8") as fichier:
        html = fichier.read()

    # Analyser le document HTML
    soup = BeautifulSoup(html, "html.parser")

    # Récupérer les blocs d'annonces
    blocs_annonces = soup.select(".annonce")

    # Créer une liste vide
    annonces = []

    for bloc in blocs_annonces:

        titre = bloc.select_one("h2").get_text(strip=True)
        prix = bloc.select_one(".prix").get_text(strip=True)
        surface = bloc.select_one(".surface").get_text(strip=True)

        prix = int(prix.replace("€", "").strip())
        surface = float(surface.replace("m²", "").strip())
        valeur_charges = bloc.get("data-charges")
        if valeur_charges == "cc":
            charges_comprises = True
        elif valeur_charges == "hc":
            charges_comprises = False
        else:
            charges_comprises = None
        
        annonce = {
            "titre": titre,
            "loyer": prix,
            "surface": surface,
            "charges_comprises": charges_comprises          
        }

        annonces.append(annonce)

    return annonces
