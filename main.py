from app import create_app
import os
import pandas as pd
from flask import Flask, render_template, jsonify
from app import create_app

# Initialiser l'application Flask
app = create_app()

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


if __name__ == "__main__":
    app.run(debug=True)







