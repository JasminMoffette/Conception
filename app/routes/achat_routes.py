from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db
# grace au init
from app.models import Achat, LigneAchat, Projet

achat_bp = Blueprint('achat', __name__)

# ====================================================
# Route pour afficher le formulaire de commande d'achat
# ====================================================
@achat_bp.route("/", methods=["GET"])
def achat():
    # Debug : afficher l'URI de la base utilisée
    print("SQLALCHEMY_DATABASE_URI:", current_app.config.get('SQLALCHEMY_DATABASE_URI'))
    # Récupération de tous les projets actifs (filtrage à ajuster si nécessaire)
    projets_actifs = Projet.query.all()
    print("Projets récupérés dans achat :", projets_actifs)
    return render_template("achat.html", projets=projets_actifs)

# ====================================================
# Route pour gérer l'upload d'un fichier de commande d'achat
# ====================================================
@achat_bp.route("/upload_commande", methods=['POST'])
def upload_commande():
    """
    Gère l'upload d'un fichier de commande d'achat.
    Si le fichier est absent ou vide, affiche un message d'erreur.
    Sinon, enregistre le fichier et utilise la méthode importer_commande pour traiter l'importation.
    """
    if 'file' not in request.files or request.files['file'].filename == '':
        flash("❌ Aucun fichier sélectionné.", "error")
        return redirect(url_for('achat_bp.achat'))

    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Créer une instance d'Achat et appeler la méthode d'importation
    achat_instance = Achat()
    achat_instance.importer_commande(file_path)

    flash(f"✅ Fichier {file.filename} importé et inventaire mis à jour !", "success")
    return redirect(url_for('achat_bp.achat'))

# ====================================================
# Route pour créer une commande d'achat manuelle (création et association des produits)
# ====================================================
@achat_bp.route("/creer", methods=["GET", "POST"])
def creer_achat():
    if request.method == "POST":
        # Récupération des données du formulaire
        po = request.form.get("po")
        date_achat = request.form.get("date_achat")
        fournisseur = request.form.get("fournisseur")
        prix = request.form.get("prix")
        projet_id = request.form.get("projet_id")  # L'ID du projet sélectionné

        # Vérification que le champ PO est renseigné
        if not po:
            return jsonify({"message": "❌ Le numéro de commande (PO) est obligatoire."}), 400

        # Conversion de la date
        try:
            date_achat_obj = datetime.strptime(date_achat, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "❌ Format de date invalide."}), 400

        try:
            # Création de l'achat
            achat_instance = Achat(po=po, date_achat=date_achat_obj, fournisseur=fournisseur, prix=prix, projet_id=projet_id)
            db.session.add(achat_instance)
            db.session.commit()

            # Récupération des données des lignes de produits
            produit_codes = request.form.getlist("produit_code[]")
            produit_descriptions = request.form.getlist("produit_description[]")
            produit_materiaux = request.form.getlist("produit_materiaux[]")
            produit_categories = request.form.getlist("produit_categorie[]")
            produit_quantites = request.form.getlist("produit_quantite[]")

            # Importation locale pour éviter les imports inutiles en début de fonction
            from app.models.produit import Produit

            # Traitement de chaque ligne de produit
            for i, code in enumerate(produit_codes):
                if not code.strip():
                    continue  # Ignorer les lignes vides
                description = produit_descriptions[i] if i < len(produit_descriptions) else ""
                materiaux = produit_materiaux[i] if i < len(produit_materiaux) else ""
                categorie = produit_categories[i] if i < len(produit_categories) else ""
                quantite = produit_quantites[i] if i < len(produit_quantites) else 0
                try:
                    quantite = int(quantite)
                except ValueError:
                    quantite = 0

                # Vérifier si le produit existe déjà, sinon le créer
                produit = Produit.query.filter_by(code=code).first()
                if not produit:
                    produit = Produit(code=code, description=description, materiaux=materiaux, categorie=categorie, quantite=0)
                    db.session.add(produit)
                    db.session.commit()  # Nécessaire pour obtenir produit.id

                # Création de la ligne d'achat pour associer le produit à l'achat
                ligne_achat = LigneAchat(quantite=quantite, achat_id=achat_instance.id, produit_id=produit.id)
                db.session.add(ligne_achat)

            db.session.commit()

            # Création d'une réception associée à l'achat
            from app.models.reception import Reception
            reception_instance = Reception(achat_id=achat_instance.id, date_reception=None)
            db.session.add(reception_instance)
            db.session.commit()

            return jsonify({"message": "✅ Commande d'achat créée avec succès et réception générée."})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"❌ Erreur lors de la création de la commande d'achat : {e}"}), 500
    else:
        # Pour la méthode GET, rediriger vers le formulaire principal
        return redirect(url_for('achat_bp.achat'))
