from flask import Blueprint, render_template, request, jsonify
from app.models.produit import Produit
from app.database import Database
from .projet import Projet


inventaire_bp = Blueprint('inventaire', __name__) 

@inventaire_bp.route("/")
def inventaire():
    return render_template("inventaire.html")

@inventaire_bp.route("/general")
def inventaire_general():
    return render_template("inventaire_general.html")

@inventaire_bp.route("/libre")
def inventaire_libre():
    return render_template("inventaire_libre.html")

@inventaire_bp.route("/inventaire_libre")
def liste_produits_libres():
    """Affiche uniquement les produits qui n'ont pas de projet et qui ont du stock disponible."""
    db = Database()
    db.cursor.execute("""
        SELECT code, description, materiaux, quantite, emplacement 
        FROM produits 
        WHERE (projet IS NULL OR projet = '' OR projet = 'None' OR projet = 'NULL')
        AND quantite > 0
    """)
    produits_libres = db.cursor.fetchall()

    print(f"✅ Produits libres récupérés par Flask : {produits_libres}")  # 🔍 Vérification console

    produits = []
    for produit in produits_libres:
        produits.append({
            "code": produit[0],
            "description": produit[1] if produit[1] else "N/A",
            "materiaux": produit[2] if produit[2] else "N/A",
            "quantite": produit[3] if produit[3] else 0,
            "emplacement": produit[4] if produit[4] else "N/A"
        })

    print(f"✅ Produits envoyés au HTML : {produits}")  # 🔍 Vérification console

    return render_template("inventaire_libre.html", produits=produits)



@inventaire_bp.route("/attribuer_projet", methods=["POST"])
def attribuer_projet():
    """Attribue une quantité d'un produit à un projet en utilisant la classe Projet."""
    data = request.json
    print(f"✅ Données reçues par Flask : {data}")

    code = data.get("code")
    projet_nom = data.get("projet")
    quantite_attribuee = int(data.get("quantite", 0))

    if not code or not projet_nom or quantite_attribuee <= 0:
        return jsonify({"message": "❌ Erreur : Code produit, projet ou quantité invalide"}), 400

    # Création du projet (s'il n'existe pas encore)
    projet = Projet(projet_nom)
    projet.ajouter_projet()

    # Attribution du produit au projet
    if projet.attribuer_produit(code, quantite_attribuee):
        return jsonify({"message": f"✅ {quantite_attribuee} unités attribuées à '{projet_nom}' pour {code}."})
    else:
        return jsonify({"message": "❌ Erreur lors de l'attribution du produit."}), 400



@inventaire_bp.route("/projet")
def inventaire_projet():
    return render_template("inventaire_projet.html")

@inventaire_bp.route("/quincaillerie")
def quincaillerie():
    return render_template("quincaillerie.html")



