from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db
from app.models.achat import Achat
from app.models.associations import LigneAchat  
from app.models.projet import Projet


achat_bp = Blueprint('achat_bp', __name__)

# ====================================================
# Route pour afficher le formulaire de commande d'achat
# ====================================================
@achat_bp.route("/", methods=["GET"])
def achat():
    print("SQLALCHEMY_DATABASE_URI:", current_app.config.get('SQLALCHEMY_DATABASE_URI'))
    # Pour le moment, on récupère tous les projets ; plus tard, on pourra ajuster le filtre
    projets_actifs = Projet.query.all()
    print("Projets récupérés dans achat :", projets_actifs)
    return render_template("achat.html", projets=projets_actifs)

# ====================================================
# Route pour gérer l'upload d'un fichier de commande d'achat
# ====================================================
@achat_bp.route("/upload_commande", methods=['POST'])
def upload_commande():
    """Gère l'upload d'un fichier commande d'achat."""
    if 'file' not in request.files or request.files['file'].filename == '':
        flash("❌ Aucun fichier sélectionné.", "error")
        return redirect(url_for('achat_bp.achat'))

    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Créer une instance d'achat pour importer la commande
    achat_module = Achat()
    achat_module.importer_commande(file_path)

    flash(f"✅ Fichier {file.filename} importé et inventaire mis à jour !", "success")
    return redirect(url_for('achat_bp.achat'))

# ====================================================
# Route pour créer une commande d'achat manuelle (création et association des produits)
# ====================================================
@achat_bp.route("/creer", methods=["GET", "POST"])
def creer_achat():
    if request.method == "POST":
        # Récupération des champs du formulaire
        po = request.form.get("po")
        date_achat = request.form.get("date_achat")
        fournisseur = request.form.get("fournisseur")
        prix = request.form.get("prix")
        projet_id = request.form.get("projet_id")  # L'ID du projet sélectionné

        # Vérification du champ obligatoire PO
        if not po:
            return jsonify({"message": "❌ Le numéro de commande (PO) est obligatoire."}), 400

        # Conversion de la date
        try:
            date_achat_obj = datetime.strptime(date_achat, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "❌ Format de date invalide."}), 400

        try:
            # Création de la commande d'achat
            achat = Achat(po=po, date_achat=date_achat_obj, fournisseur=fournisseur, prix=prix, projet_id=projet_id)
            db.session.add(achat)
            db.session.commit()

            # Traitement dynamique des lignes de produits
            produit_codes = request.form.getlist("produit_code[]")
            produit_descriptions = request.form.getlist("produit_description[]")
            produit_materiaux = request.form.getlist("produit_materiaux[]")
            produit_categories = request.form.getlist("produit_categorie[]")
            produit_quantites = request.form.getlist("produit_quantite[]")

            from app.models.produit import Produit

            for i, code in enumerate(produit_codes):
                if code.strip() == "":
                    continue  # Ignorer les lignes vides
                description = produit_descriptions[i] if i < len(produit_descriptions) else ""
                materiaux = produit_materiaux[i] if i < len(produit_materiaux) else ""
                categorie = produit_categories[i] if i < len(produit_categories) else ""
                quantite = produit_quantites[i] if i < len(produit_quantites) else 0
                try:
                    quantite = int(quantite)
                except ValueError:
                    quantite = 0

                # Vérifier l'existence du produit, sinon le créer
                produit = Produit.query.filter_by(code=code).first()
                if not produit:
                    produit = Produit(code=code, description=description, materiaux=materiaux, categorie=categorie, quantite=0)
                    db.session.add(produit)
                    db.session.commit()  # Pour obtenir produit.id

                # Création de la ligne d'achat associant le produit à la commande
                ligne_achat = LigneAchat(quantite=quantite, achat_id=achat.id, produit_id=produit.id)
                db.session.add(ligne_achat)

            db.session.commit()

            # Création d'une réception associée à la commande
            from app.models.reception import Reception
            reception = Reception(achat_id=achat.id, date_reception=None)
            db.session.add(reception)
            db.session.commit()

            return jsonify({"message": "✅ Commande d'achat créée avec succès et réception générée."})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"❌ Erreur lors de la création de la commande d'achat : {e}"}), 500
    else:
        # Pour GET, rediriger vers le formulaire principal
        return redirect(url_for('achat_bp.achat'))
