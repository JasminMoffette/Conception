from flask import Blueprint, render_template, jsonify, current_app

main_bp = Blueprint("main", __name__)

# ====================================================
# Route principale de l'application
# ====================================================
@main_bp.route("/")
def index():
    """Affiche la page d'accueil."""
    return render_template("index.html")

# ====================================================
# Route pour afficher le plan de l'usine
# ====================================================
@main_bp.route("/plan")
def plan():
    """Affiche la page du plan de l'usine."""
    return render_template("plan.html")


# ====================================================
# Création de routes dynamiques pour certains modules
# ====================================================
def render_dynamic_module(module_name):
    """
    Rendu dynamique d'un module via son template correspondant (par exemple, 'achat.html').
    """
    return render_template(f"{module_name}.html")

def creer_routes_dynamiques(blueprint):
    """
    Ajoute dynamiquement des routes pour les modules spécifiés.
    Les modules ciblés sont : "achat", "reception", "inventaire", "production" et "ajustement".
    Chaque route est ajoutée sous la forme "/<module>" et rend le template correspondant.
    """
    modules = ["achat", "reception", "inventaire", "production", "ajustement"]
    for module in modules:
        # Utilisation d'une closure pour capturer la valeur actuelle de module
        blueprint.add_url_rule(
            f"/{module}", module, (lambda m: lambda: render_dynamic_module(m))(module)
        )

# Ajout des routes dynamiques au blueprint main_bp
creer_routes_dynamiques(main_bp)
