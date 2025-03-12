from .main_routes import main_bp
from .inventaire_routes import inventaire_bp
from .achat_routes import achat_bp
from .reception_routes import reception_bp
from .production_routes import production_bp
from .ajustement_routes import ajustement_bp
from .emplacement_routes import emplacement_bp
from .entrepot_routes import entrepot_bp
from .projet_routes import projet_bp




def register_blueprints(app):
    """Enregistre tous les blueprints dans l'application Flask."""
    # Routes principales (page d'accueil, etc.)
    app.register_blueprint(main_bp)
    # Routes d'inventaire
    app.register_blueprint(inventaire_bp, url_prefix="/inventaire")
    # Routes d'achat
    app.register_blueprint(achat_bp, url_prefix="/achat")
    # Routes de réception
    app.register_blueprint(reception_bp, url_prefix="/reception")
    # Routes de production
    app.register_blueprint(production_bp, url_prefix="/production")
    # Routes d'ajustement
    app.register_blueprint(ajustement_bp, url_prefix="/ajustement")
    # Routes d'emplacement
    app.register_blueprint(emplacement_bp, url_prefix="/emplacement")
    # Routes d'entrepôt
    app.register_blueprint(entrepot_bp)
    # Routes de projet
    app.register_blueprint(projet_bp, url_prefix="/projet")

  










