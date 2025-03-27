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
    # Récupérer le code produit, champ obligatoire
    code = request.form.get("code")
    if not code:
        flash("❌ Le code produit est obligatoire.", "error")
        return redirect(url_for("ajustement.ajustement"))

    # Récupérer les autres attributs facultatifs depuis le formulaire
    valid_attributs = {}
    for key in ["description", "materiaux", "categorie", "quantite"]:
        value = request.form.get(key)
        if value:
            # Pour 'quantite', on essaie de convertir en entier
            if key == "quantite":
                try:
                    value = int(value)
                except ValueError:
                    flash("❌ La quantité doit être un nombre entier.", "error")
                    return redirect(url_for("ajustement.ajustement"))
            valid_attributs[key] = value

    # Vérifier si le produit existe déjà dans la base de données
    produit_existant = Produit.query.filter_by(code=code).first()
    if produit_existant:
        flash(f"⚠️ Le produit {code} existe déjà.", "warning")
        return redirect(url_for("ajustement.ajustement"))

    # Créer et enregistrer le nouveau produit
    nouveau_produit = Produit(code=code, **valid_attributs)
    db.session.add(nouveau_produit)
    db.session.commit()

    flash(f"✅ Produit {code} ajouté avec succès à l'inventaire !", "success")
    return redirect(url_for("ajustement.ajustement"))
