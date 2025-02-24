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

    # Importer et enregistrer les routes (BluePrints)
    from app.routes.main_routes import main_bp
    from app.routes.achat_routes import achat_bp
    from app.routes.ajustement_routes import ajustement_bp
    from app.routes.emplacement_routes import emplacement_bp
    from app.routes.reception_routes import reception_bp
    from app.routes.production_routes import production_bp
    from app.routes.inventaire_routes import inventaire_bp
    

    app.register_blueprint(main_bp)
    app.register_blueprint(achat_bp, url_prefix="/achat")
    app.register_blueprint(ajustement_bp, url_prefix="/ajustement")
    app.register_blueprint(emplacement_bp, url_prefix="/emplacement")
    app.register_blueprint(reception_bp, url_prefix="/reception")
    app.register_blueprint(production_bp, url_prefix="/producion")
    app.register_blueprint(inventaire_bp, url_prefix="/inventaire")

    return app
