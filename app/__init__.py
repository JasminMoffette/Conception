from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import pandas as pd
import os

# Initialisation de SQLAlchemy et Flask-Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Initialise l'application Flask avec ses configurations et modules nécessaires."""
    app = Flask(__name__)

    # Charger la configuration depuis l'objet Config
    app.config.from_object(Config)

    # Charger le fichier Excel
    excel_path = os.path.join(Config.DATA_FOLDER, "DATA_Plan_entrepot.xlsx")
    if not os.path.exists(excel_path):
        print(f"❌ ERREUR : Fichier Excel introuvable à {excel_path}")
        app.config["df_excel"] = None  # On évite une erreur si le fichier est absent
    else:
        df_excel = pd.read_excel(excel_path, sheet_name=None)  # Charge toutes les feuilles Excel
        app.config["df_excel"] = df_excel
        print(f"✅ Fichier Excel chargé avec succès. Feuilles disponibles : {list(df_excel.keys())}")

    # Initialiser les extensions (SQLAlchemy, Flask-Migrate)
    db.init_app(app)
    migrate.init_app(app, db)

    # Enregistrer les blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app



