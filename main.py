import os
import pandas as pd
from flask import Flask
from app import create_app

# Initialiser l'application Flask

app = create_app()


# Charger les données Excel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "DATA_Plan_entrepot.xlsx")

def charger_donnees_excel():
    """ Vérifie et charge le fichier Excel si disponible. """
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ ERREUR : Fichier '{EXCEL_PATH}' introuvable.")
        return None
    return pd.read_excel(EXCEL_PATH, sheet_name=None)  # Charge toutes les feuilles

# Charger les données Excel et les rendre accessibles dans Flask
df_excel = charger_donnees_excel()
app.config["df_excel"] = df_excel  # ✅ Vérifie que cette ligne est bien présente

if __name__ == "__main__":
    app.run(debug=True)
