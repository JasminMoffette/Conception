from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.produit import Produit
from app import db

ajustement_bp = Blueprint("ajustement", __name__)

# ====================================================
# Route d'affichage de la page d'ajustement (formulaire)
# ====================================================
@ajustement_bp.route("/", methods=["GET"])
def ajustement():

    if "user_type" not in session or session["user_type"] != "gestionnaire":
        return "Acces refusé"

    return render_template("ajustement.html")

# ====================================================
# Route pour créer un nouveau produit via le formulaire d'ajustement
# ====================================================
@ajustement_bp.route("/creer_produit", methods=["POST"])
def creer_produit():
    code = request.form.get("code")
    if not code:  
        code = None

    valid_attributs = {}
    for key in ["description", "materiaux", "categorie", "quantite"]:
        value = request.form.get(key)
        if value:
            if key == "quantite":
                try:
                    value = int(value)
                except ValueError:
                    flash("❌ La quantité doit être un nombre entier.", "error")
                    return redirect(url_for("ajustement.ajustement"))
            valid_attributs[key] = value

    try:
        nouveau_produit = Produit(code=code, **valid_attributs)
        nouveau_produit.crer_produit()
        flash(f"✅ Produit {code} ajouté avec succès à l'inventaire !", "success")
    except ValueError as e:
        flash(f"⚠️ {str(e)}", "warning")
    except Exception as e:
        flash(f"❌ Erreur inattendue : {str(e)}", "error")

    return redirect(url_for("ajustement.ajustement"))

