from flask import Blueprint, render_template,  request, redirect, url_for, session,flash
from app.models.utilisateur import Utilisateur
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

# ====================================================
# Routes pour les logins
# ====================================================
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Utilisateur.query.filter_by(nom=username).first()

        if user and user.mot_de_passe == password: 
            session["user_type"] = user.poste
            session["username"] = user.nom
            flash(f"Connexion à {user.nom} - {user.poste}", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Identifiant ou mot de passe incorrect", "danger")
            return render_template("login.html")

    return render_template("login.html")

#=================================================
#Route pour les logouts
#=================================================
@main_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_type', None)
    session.pop('username', None)
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('main.index'))