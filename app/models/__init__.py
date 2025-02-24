from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialisation de la base de données
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Initialise l'application Flask avec les configurations et les modules nécessaires."""
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialisation de la base de données
    db.init_app(app)
    migrate.init_app(app, db)

    # Importer et enregistrer les Blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app

