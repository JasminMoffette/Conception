from flask import Blueprint, render_template, request, jsonify
from app.models.produit import Produit
from app.models.projet import Projet  
from app import db

inventaire_bp = Blueprint('inventaire', __name__) 

@inventaire_bp.route("/")
def inventaire():
    return render_template("inventaire.html")

@inventaire_bp.route("/inventaire_projet")
def inventaire_projet():
    return render_template("inventaire_projet.html")

@inventaire_bp.route("/general")
def inventaire_general():
    return render_template("inventaire_general.html")

@inventaire_bp.route("/libre")
def inventaire_libre():
    produits_libres = Produit.query.filter(~Produit.projets_associes.any()).all()

    return render_template("inventaire_libre.html", produits=produits_libres)

@inventaire_bp.route("/quincaillerie")
def quincaillerie():
    return render_template("quincaillerie.html")

@inventaire_bp.route("/attribuer_projet", methods=["POST"])
def attribuer_projet():
    data = request.json
    code = data.get("code")
    projet_nom = data.get("projet")
    quantite = data.get("quantite")

    if not code or not projet_nom or not quantite:
        return jsonify({"message": "❌ Données manquantes ou invalides."}), 400

    produit = Produit.query.filter_by(code=code).first()
    if not produit:
        return jsonify({"error": "Produit non trouvé."}), 404

    # Vérifie ou crée le projet
    projet = Projet.query.filter_by(nom=projet_nom).first()
    if not projet:
        projet = Projet(nom=projet_nom)
        db.session.add(projet)
        db.session.commit()

    # Attribution du produit au projet
    produit.projet = projet.nom
    db.session.commit()

    return jsonify({"message": f"✅ Produit {code} attribué au projet {projet_nom}."})

