from .main_routes import main_bp
from .inventaire_routes import inventaire_bp  
from .achat_routes import achat_bp
from .reception_routes import reception_bp
from .production_routes import production_bp
from .ajustement_routes import ajustement_bp
from .emplacement_routes import emplacement_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(inventaire_bp, url_prefix="/inventaire")  
    app.register_blueprint(achat_bp, url_prefix="/achat")
    app.register_blueprint(reception_bp, url_prefix="/reception")
    app.register_blueprint(production_bp, url_prefix="/production")
    app.register_blueprint(ajustement_bp, url_prefix="/ajustement")
    app.register_blueprint(emplacement_bp, url_prefix="/emplacement")







