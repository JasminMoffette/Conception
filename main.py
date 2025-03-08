import os
import pandas as pd
from flask import Flask
from app import create_app
import logging
import webbrowser
import threading
from config import Config

# Réduire les logs inutiles
logging.basicConfig(level=logging.ERROR)

# Initialisation de l'application Flask
app = create_app()

# Charger les données Excel uniquement si elles existent
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construction du chemin vers le fichier Excel à partir de la config
EXCEL_PATH = os.path.join(Config.DATA_FOLDER, "DATA_Plan_entrepot.xlsx")

def charger_donnees_excel():
    """Charge le fichier Excel s'il est disponible."""
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ ERREUR : Fichier '{EXCEL_PATH}' introuvable.")
        return None
    print("✅ Fichier Excel pour les plans d'entrepot chargé avec succès.")
    return pd.read_excel(EXCEL_PATH, sheet_name=None)  # Charge toutes les feuilles

df_excel = charger_donnees_excel()

# Ajouter les données Excel dans Flask si elles sont chargées
if df_excel is not None:
    app.config["df_excel"] = df_excel  # ✅ Ne pas exécuter si `df_excel` est None

def open_browser():
    """Ouvre automatiquement le navigateur sur l'URL de l'application."""
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()  
    app.run(debug=True)
