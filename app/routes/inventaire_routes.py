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
    projets = Projet.query.all()
    return render_template("inventaire_projet.html", projets=projets)


@inventaire_bp.route("/general")
def inventaire_general():
    return render_template("inventaire_general.html")

@inventaire_bp.route("/libre")
def inventaire_libre():
    # Affiche tous les produits dont la quantité disponible est supérieure à zéro
    produits_libres = Produit.query.filter(Produit.quantite > 0).all()
    return render_template("inventaire_libre.html", produits=produits_libres)

@inventaire_bp.route("/quincaillerie")
def quincaillerie():
    return render_template("quincaillerie.html")

@inventaire_bp.route("/attribuer_projet", methods=["POST"])
def attribuer_projet():
    data = request.json
    code = data.get("code")
    projet_code = data.get("projet")  # on attend le code du projet ici
    quantite = data.get("quantite")

    # Validation des données
    if not code or not projet_code or not quantite:
        return jsonify({"message": "❌ Données manquantes ou invalides."}), 400

    # Récupérer le produit par son code
    produit = Produit.query.filter_by(code=code).first()
    if not produit:
        return jsonify({"message": "❌ Produit non trouvé."}), 404

    # Vérifier la disponibilité du stock
    if produit.quantite < quantite:
        return jsonify({"message": "❌ Quantité insuffisante."}), 400

    # Récupérer le projet par son code, ou le créer s'il n'existe pas
    projet = Projet.query.filter_by(code=projet_code).first()
    if not projet:
        projet = Projet(code=projet_code)
        db.session.add(projet)
        db.session.commit()

    # Importer le modèle d'association
    from app.models.associations import ProduitProjet

    # Rechercher une association existante entre ce produit et ce projet
    association = ProduitProjet.query.filter_by(produit_id=produit.id, projet_id=projet.id).first()
    if association:
        # Ajouter la quantité demandée à l'association existante
        association.quantite += quantite
    else:
        # Créer une nouvelle association
        association = ProduitProjet(produit_id=produit.id, projet_id=projet.id, quantite=quantite)
        db.session.add(association)

    # Mettre à jour le stock du produit
    produit.quantite -= quantite

    try:
        db.session.commit()
        return jsonify({"message": f"✅ Produit {code} attribué au projet {projet.code} avec {quantite} unités."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"❌ Erreur lors de l'attribution : {e}"}), 500
    

@inventaire_bp.route("/projet_liste")
def projet_liste():
    # Récupérer le code du projet depuis les paramètres GET
    projet_code = request.args.get("projet")
    if not projet_code:
        return "Aucun projet sélectionné.", 400

    from app.models.projet import Projet
    from app.models.associations import ProduitProjet
    from app.models.produit import Produit

    # Récupérer le projet
    projet = Projet.query.filter_by(code=projet_code).first()
    if not projet:
        return f"Projet '{projet_code}' non trouvé.", 404

    # Récupérer toutes les associations pour ce projet
    associations = ProduitProjet.query.filter_by(projet_id=projet.id).all()

    # Préparer une liste d'informations pour le rendu
    inventaire = []
    for assoc in associations:
        produit = Produit.query.get(assoc.produit_id)
        if produit:
            inventaire.append({
                "code": produit.code,
                "description": produit.description,
                "materiaux": produit.materiaux,
                "quantite": assoc.quantite
            })

    # Rendu d'un template partiel pour afficher l'inventaire
    return render_template("inventaire_projet_liste.html", inventaire=inventaire, projet=projet)



