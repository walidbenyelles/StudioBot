
import requests
from bs4 import BeautifulSoup

# Étape 1 : récupérer le HTML
url = "https://books.toscrape.com/"

reponse = requests.get(url, timeout=10)
reponse.raise_for_status()

# Étape 2 : analyser le HTML
soup = BeautifulSoup(reponse.text, "html.parser")

# Étape 3 : trouver les livres
livres = soup.select("article.product_pod")

print("Nombre de livres :", len(livres))

# Étape 4 : extraire les informations
for livre in livres:

    lien = livre.select_one("h3 a")
    prix_element = livre.select_one(".price_color")

    titre = lien.get("title")
    prix = prix_element.get_text(strip=True)
    url_livre = lien.get("href")

    print("Titre :", titre)
    print("Prix :", prix)
    print("Lien :", url_livre)
    print("------------------------")
