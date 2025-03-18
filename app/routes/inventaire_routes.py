from flask import Blueprint, render_template, request, jsonify
from app.models.produit import Produit
from app.models.projet import Projet  
from app import db

inventaire_bp = Blueprint('inventaire', __name__)

# ====================================================
# Route d'affichage de la page principale d'inventaire
# ====================================================
@inventaire_bp.route("/")
def inventaire():
    """
    Affiche la page d'accueil de l'inventaire.
    """
    return render_template("inventaire.html")

# ====================================================
# Route d'affichage des projets actifs pour l'inventaire par projet
# ====================================================
@inventaire_bp.route("/inventaire_projet")
def inventaire_projet():
    """
    Affiche la page de sélection des projets actifs pour l'inventaire.
    Ici, on filtre les projets dont le statut est "en cours".
    """
    projets_actifs = Projet.query.filter_by(statut="en cours").all()
    return render_template("inventaire_projet.html", projets=projets_actifs)

# ====================================================
# Route d'affichage de l'inventaire général (tous les produits)
# ====================================================
@inventaire_bp.route("/general")
def inventaire_general():
    """
    Affiche l'inventaire général regroupant tous les produits.
    """
    produits = Produit.query.all()
    return render_template("inventaire_general.html", produits=produits)

# ====================================================
# Route d'affichage de l'inventaire des produits libres
# ====================================================
@inventaire_bp.route("/libre")
def inventaire_libre():
    """
    Affiche l'inventaire des produits disposant d'une quantité libre.
    La quantité libre est calculée comme la différence entre la quantité en stock 
    et la quantité déjà attribuée à des projets.
    """
    produits = Produit.query.all()
    produits_libres = []
    for produit in produits:
        # Calcul de la quantité déjà attribuée via les associations avec les projets
        total_attribue = sum(assoc.quantite for assoc in produit.projets_associes)
        free = produit.quantite - total_attribue
        if free > 0:
            # Ajout d'un attribut 'free' à l'objet produit pour le rendu
            produit.free = free
            produits_libres.append(produit)
    return render_template("inventaire_libre.html", produits=produits_libres)

# ====================================================
# Route pour afficher la page d'inventaire par entrepôt
# ====================================================
@inventaire_bp.route("/inventaire_entrepot")
def inventaire_entrepot():
    """
    Affiche la page dédiée à l'inventaire par entrepôt.
    """
    return render_template("inventaire_entrepot.html")

# ====================================================
# Route pour attribuer un produit à un projet
# ====================================================
@inventaire_bp.route("/attribuer_projet", methods=["POST"])
def attribuer_projet():
    """
    Attribue un produit à un projet en créant ou en mettant à jour une association.
    Les données sont envoyées au format JSON et doivent contenir :
      - code : le code du produit
      - projet : le code du projet
      - quantite : la quantité à attribuer
    """
    data = request.json
    code = data.get("code")
    projet_code = data.get("projet")
    quantite = data.get("quantite")

    # Validation des données reçues
    if not code or not projet_code or not quantite:
        return jsonify({"message": "❌ Données manquantes ou invalides."}), 400

    # Récupération du produit
    produit = Produit.query.filter_by(code=code).first()
    if not produit:
        return jsonify({"message": "❌ Produit non trouvé."}), 404

    # Vérification de la disponibilité du stock
    if produit.quantite < quantite:
        return jsonify({"message": "❌ Quantité insuffisante."}), 400

    # Récupération ou création du projet en fonction du code
    projet = Projet.query.filter_by(code=projet_code).first()
    if not projet:
        projet = Projet(code=projet_code)
        db.session.add(projet)
        db.session.commit()

    # Import local du modèle d'association
    from app.models.associations import ProduitProjet

    # Recherche d'une association existante
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
# Route pour afficher l'inventaire détaillé d'un projet
# ====================================================
@inventaire_bp.route("/projet_liste")
def projet_liste():
    """
    Affiche l'inventaire détaillé d'un projet donné.
    Le code du projet est passé en paramètre GET.
    """
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

    # Récupérer les associations pour ce projet
    associations = ProduitProjet.query.filter_by(projet_id=projet.id).all()

    # Préparer les données d'inventaire pour le rendu
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



@inventaire_bp.route("/entrepot_detail")
def inventaire_entrepot_detail():
     entrepot = request.args.get("entrepot")
     if not entrepot:
         return "Aucun entrepôt sélectionné.", 400
 
     # Récupérer les produits pour cet entrepôt (selon votre logique)
     # Ici, on suppose que l'emplacement du produit est enregistré dans un attribut stock.cellule
     # et que vous avez une relation entre Produit et Stock.
     produits = Produit.query.filter(Produit.stocks.any(Stock.entrepot == entrepot)).all()
     
     return render_template("inventaire_entrepot_detail.html", produits=produits, entrepot=entrepot)

