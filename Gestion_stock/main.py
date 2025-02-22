import os
import pandas as pd
from flask import Flask, render_template, jsonify
from routes import setup_routes  # Import des routes depuis un module séparé

# Initialiser l'application Flask
app = Flask(__name__)

# Récupérer le chemin absolu du dossier contenant ce fichier
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "DATA_Plan_entrepot.xlsx")

# Charger les données depuis le fichier Excel
def charger_donnees_excel():
    """ Vérifie et charge le fichier Excel si disponible. """
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ ERREUR : Fichier '{EXCEL_PATH}' introuvable.")
        return None
    return pd.read_excel(EXCEL_PATH, sheet_name=None)  # Charge toutes les feuilles

df_excel = charger_donnees_excel()

# Configuration des routes Flask
setup_routes(app, df_excel)

if __name__ == "__main__":
    print("Lancement de l'application Flask...")
    app.run(debug=True)





######   TEST  ##############

print("✅ Test des fonctionnalités de l'inventaire...")
achat_test = achat.Achat(projet="001")
produits_test = [
    produit.Produit("Ordinateur portable", "OP001", "Électronique", po="PO12345", quantite=5),
    produit.Produit("Souris sans fil", "SS001", "Accessoire", po="PO12345", emplacement="Étagère A", quantite=20),
    produit.Produit("Écran 24 pouces", "EC001", "Électronique", po="PO12346", dimension="24x18x2", quantite=10),
    produit.Produit("Clavier mécanique", "CM001", "Accessoire", po="PO12347", emplacement="Étagère B", dimension="18x6x1", quantite=15),
    produit.Produit("Câble HDMI", "CH001", "Accessoire", po="PO12348", quantite=50)
]

inventaire_test = inventaire.Inventaire("001")
for i in produits_test:
    inventaire_test.ajouter_produit(i)

repertoire_test = repertoire.Repertoire()
repertoire_test.ajouter_inventaire(inventaire_test)

print(inventaire_test.produits)
print(produits_test[0])
print(produits_test)
print(repertoire_test.inventaires)
print(inventaire_test)

