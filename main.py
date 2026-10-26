
from scraper import extraire_annonces


def verifier_annonce(annonce):

    if annonce["loyer"] > 700:
        return "REJETEE", "Loyer trop élevé"

    if annonce["surface"] < 13:
        return "REJETEE", "Surface trop petite"

    if annonce["charges_comprises"] is not True:
        return "A_VERIFIER", "Loyer charges comprises non confirmé"

    return "PRESELECTIONNEE", "Critères initiaux respectés"


annonces = extraire_annonces()

print("Nombre d'annonces :", len(annonces))

for annonce in annonces:

    statut, raison = verifier_annonce(annonce)

    print(annonce["titre"], ":", statut, "-", raison)
