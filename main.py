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







