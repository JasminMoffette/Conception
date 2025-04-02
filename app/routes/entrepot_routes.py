from flask import Blueprint, render_template, jsonify, current_app
from app.models import Emplacement, Stock

entrepot_bp = Blueprint('entrepot', __name__)

# ====================================================
# Route pour afficher l'intérieur d'un entrepôt spécifique
# ====================================================
@entrepot_bp.route("/<nom>")
def afficher_entrepot(nom):
    from flask import request  # à ajouter en haut si pas déjà
    mode = request.args.get("mode", "reception")  # défaut = mode réception

    # Récupérer les données Excel comme avant...
    df_excel = current_app.config.get("df_excel")
    if df_excel is None:
        return render_template("erreur.html", message="Fichier Excel introuvable."), 500

    feuille = nom.lower().replace(" ", "_")
    if feuille not in df_excel:
        return render_template("erreur.html", message=f"Aucun plan disponible pour l'entrepôt {nom}."), 404

    df_interieur = df_excel[feuille]

    required_columns_elements = {"Value", "Position X", "Position Y"}
    required_columns_murs = {"Start X", "Start Y", "End X", "End Y"}
    if required_columns_elements - set(df_interieur.columns):
        return render_template("erreur.html", message="Colonnes manquantes pour les emplacements."), 500
    if required_columns_murs - set(df_interieur.columns):
        return render_template("erreur.html", message="Colonnes manquantes pour les murs."), 500

    entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    murs_data = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    for element in entrepot_data:
        cellule_nom = element["Value"]
        emplacement = Emplacement.query.filter_by(entrepot=nom, cellule=cellule_nom).first()
        if emplacement:
            element["id"] = emplacement.id
            stock_exist = Stock.query.filter(Stock.emplacement_id == emplacement.id, Stock.quantite > 0).first()
            element["occupee"] = stock_exist is not None
        else:
            element["occupee"] = False

    # 🧠 Choix du bon template
    if mode == "inventaire":
        return render_template("inventaire_entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)
    else:
        return render_template("entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)



@entrepot_bp.route("/api/cellule/<int:emplacement_id>")
def details_cellule(emplacement_id):
    stocks = Stock.query.filter_by(emplacement_id=emplacement_id).all()

    resultat = []
    for stock in stocks:
        produit = stock.produit
        achat = stock.achat  # récupération via achat_id
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
