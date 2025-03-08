from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.produit import Produit
from app import db

ajustement_bp = Blueprint("ajustement", __name__)

@ajustement_bp.route("/", methods=["GET"])
def ajustement():
    return render_template("ajustement.html")

@ajustement_bp.route("/creer_produit", methods=["POST"])
def creer_produit():
    code = request.form.get("code")

    if not code:
        flash("❌ Le code produit est obligatoire.", "error")
        return redirect(url_for("ajustement.ajustement"))

    valid_attributs = {
        key: request.form.get(key)
        for key in ["description", "materiaux", "categorie", "po",
                    "emplacement", "dimension", "projet", "quantite",
                    "cp", "fournisseur", "coupe", "no_catalogue", "fsc"]
        if request.form.get(key)
    }

    produit_existant = Produit.query.filter_by(code=code).first()

    if produit_existant:
        flash(f"⚠️ Le produit {code} existe déjà.", "warning")
        return redirect(url_for("ajustement.ajustement"))

    nouveau_produit = Produit(code=code, **valid_attributs)

    # Ajoute clairement ici via SQLAlchemy
    db.session.add(nouveau_produit)
    db.session.commit()

    flash(f"✅ Produit {code} ajouté avec succès à l'inventaire !", "success")
    return redirect(url_for("ajustement.ajustement"))
