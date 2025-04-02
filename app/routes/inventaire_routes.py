from flask import Blueprint, render_template, request, redirect, jsonify, current_app
from app.models import Produit, Projet, Emplacement, ProduitProjet, Stock
from app import db

inventaire_bp = Blueprint('inventaire', __name__)

# ====================================================
# Route d'accueil du module Inventaire
# ====================================================
@inventaire_bp.route("/")
def inventaire():
    return render_template("inventaire.html")

# ====================================================
# Inventaire général : tous les produits
# ====================================================
@inventaire_bp.route("/general")
def inventaire_general():
    produits = Produit.query.all()
    return render_template("inventaire_general.html", produits=produits)

# ====================================================
# Inventaire des produits libres (non attribués à un projet)
# ====================================================
@inventaire_bp.route("/libre")
def inventaire_libre():
    produits = Produit.query.all()
    produits_libres = []
    for produit in produits:
        total_attribue = sum(assoc.quantite for assoc in produit.projets_associes)
        free = produit.quantite - total_attribue
        if free > 0:
            produit.free = free
            produits_libres.append(produit)
    return render_template("inventaire_libre.html", produits=produits_libres)

# ====================================================
# Inventaire par projet (sélection d'un projet)
# ====================================================
@inventaire_bp.route("/inventaire_projet")
def inventaire_projet():
    projets_actifs = Projet.query.filter_by(statut="en cours").all()
    return render_template("inventaire_projet.html", projets=projets_actifs)

# ====================================================
# Inventaire détaillé d'un projet sélectionné
# ====================================================
@inventaire_bp.route("/projet_liste")
def projet_liste():
    projet_code = request.args.get("projet")
    if not projet_code:
        return "Aucun projet sélectionné.", 400

    projet = Projet.query.filter_by(code=projet_code).first()
    if not projet:
        return f"Projet '{projet_code}' non trouvé.", 404

    associations = ProduitProjet.query.filter_by(projet_id=projet.id).all()

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

    return render_template("inventaire_projet_liste.html", inventaire=inventaire, projet=projet)

# ====================================================
# Attribution d'un produit à un projet (via POST JSON)
# ====================================================
@inventaire_bp.route("/attribuer_projet", methods=["POST"])
def attribuer_projet():
    data = request.json
    code = data.get("code")
    projet_code = data.get("projet")
    quantite = data.get("quantite")

    if not code or not projet_code or not quantite:
        return jsonify({"message": "❌ Données manquantes ou invalides."}), 400

    produit = Produit.query.filter_by(code=code).first()
    if not produit:
        return jsonify({"message": "❌ Produit non trouvé."}), 404

    if produit.quantite < quantite:
        return jsonify({"message": "❌ Quantité insuffisante."}), 400

    projet = Projet.query.filter_by(code=projet_code).first()
    if not projet:
        projet = Projet(code=projet_code)
        db.session.add(projet)
        db.session.commit()

    association = ProduitProjet.query.filter_by(produit_id=produit.id, projet_id=projet.id).first()
    if association:
        association.quantite += quantite
    else:
        association = ProduitProjet(produit_id=produit.id, projet_id=projet.id, quantite=quantite)
        db.session.add(association)

    try:
        db.session.commit()
        return jsonify({"message": f"✅ Produit {code} attribué au projet {projet.code} avec {quantite} unités."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"❌ Erreur lors de l'attribution : {e}"}), 500

# ====================================================
# Page d'inventaire par entrepôt (choix visuel)
# ====================================================
@inventaire_bp.route("/inventaire_entrepot")
def inventaire_entrepot():
    return render_template("inventaire_entrepot.html")

# ====================================================
# Détail d'un entrepôt avec plan visuel (inventaire)
# ====================================================
@inventaire_bp.route("/entrepot/<nom>")
def inventaire_entrepot_vue(nom):
    df_excel = current_app.config.get("df_excel")
    feuille = nom.lower().replace(" ", "_")

    if df_excel is None or feuille not in df_excel:
        return "Plan introuvable pour cet entrepôt.", 404

    df = df_excel[feuille]
    elements = df.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    murs = df.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    for el in elements:
        emplacement = Emplacement.query.filter_by(entrepot=nom, cellule=el["Value"]).first()
        el["occupee"] = emplacement and Stock.query.filter(Stock.emplacement_id == emplacement.id, Stock.quantite > 0).first() is not None
        el["id"] = emplacement.id if emplacement else -1

    return render_template("inventaire_entrepot.html", entrepot=nom, elements=elements, murs=murs)

# ====================================================
# API pour récupérer les stocks d'une cellule (emplacement)
# ====================================================
@inventaire_bp.route("/api/cellule/<int:emplacement_id>")
def api_details_cellule(emplacement_id):
    stocks = Stock.query.filter_by(emplacement_id=emplacement_id).all()
    resultat = []
    for stock in stocks:
        produit = stock.produit
        achat = stock.achat
        projet_nom = achat.projet.nom if achat and achat.projet else "N/A"
        commande_po = achat.po if achat else "N/A"

        resultat.append({
            "produit_code": produit.code,
            "description": produit.description,
            "quantite": stock.quantite,
            "commande_po": commande_po,
            "projet_nom": projet_nom
        })

    return jsonify(resultat)
    
@inventaire_bp.route("/entrepot_detail")
def inventaire_entrepot_detail():
    entrepot = request.args.get("entrepot")
    if not entrepot:
        return "Aucun entrepôt sélectionné.", 400

    return redirect(f"/entrepot/{entrepot}?mode=inventaire")
