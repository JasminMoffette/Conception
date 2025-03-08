from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


# Initialisation de SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Initialise l'application Flask avec les configurations et les modules nécessaires."""
    app = Flask(__name__)

    # Charger la configuration depuis config.py
    app.config.from_object("config.Config")

    # Initialiser la base de données avec SQLAlchemy et Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Enregistrer les routes (Blueprints) depuis `routes/__init__.py`
    from app.routes import register_blueprints
    register_blueprints(app)  # ✅ Utilisation propre de l'import centralisé

    return app

