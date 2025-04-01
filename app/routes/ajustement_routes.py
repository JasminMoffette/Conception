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
    try:
        produit = Produit.creer_depuis_formulaire(request.form)
        flash(f"✅ Produit {produit.code or 'sans code'} ajouté avec succès", "success")
    except ValueError as e:
        flash(f"⚠️ {str(e)}", "warning")
    except Exception as e:
        flash(f"❌ Erreur inattendue : {str(e)}", "error")

    return redirect(url_for("ajustement.ajustement"))

