from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.produit import Produit

# Vérifie qu'il n'y a qu'UNE SEULE définition de ce Blueprint
ajustement_bp = Blueprint("ajustement", __name__)  # ✅ Nom unique

@ajustement_bp.route("/", methods=["GET"])
def ajustement():
    return render_template("ajustement.html")

@ajustement_bp.route("/creer_produit", methods=["POST"])
def creer_produit():
    code = request.form.get("code")
    if not code:
        flash("❌ Le code produit est obligatoire.", "error")
        return redirect(url_for("ajustement.ajustement"))

    attributs = {key: request.form.get(key) for key in request.form.keys() if key != "code" and request.form.get(key)}
    # Filtrer les attributs pour éviter ceux qui ne sont pas reconnus par Produit
    valid_attributs = {key: request.form.get(key) for key in ["description", "materiaux", "categorie", "po",
                                                            "emplacement", "dimension", "projet", "quantite",
                                                            "cp", "fournisseur", "coupe", "no_catalogue", "fsc"]
                    if request.form.get(key)}

    produit = Produit(code, **valid_attributs)  # ✅ Seuls les attributs valides sont passés à Produit

    produit.ajouter_produit()

    flash(f"✅ Produit {code} créer et ajouté avec succès à l'inventaire !", "success")
    return redirect(url_for("ajustement.ajustement"))





