from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.models.projet import Projet
from app.models.achat import Achat
from app.models.reception import Reception
from app.models.associations import LigneReception
from app import db

reception_bp = Blueprint('reception', __name__)

# ====================================================
# Page principale du module Réception
# Permet de sélectionner un projet (et par la suite une commande d'achat)
# ====================================================
@reception_bp.route("/", methods=["GET"])
def reception():
    """
    Affiche la page principale du module Réception.
    L'utilisateur peut y sélectionner un projet parmi ceux en cours.
    """
    projets_actifs = Projet.query.filter_by(statut="en cours").all()
    current_app.logger.info(f"Projets actifs récupérés: {len(projets_actifs)}")
    return render_template("reception.html", projets=projets_actifs)

# ====================================================
# API pour récupérer les commandes d'achat associées à un projet
# ====================================================
@reception_bp.route("/api/commandes/<int:projet_id>", methods=["GET"])
def get_commandes_by_projet(projet_id):
    """
    Retourne la liste des commandes d'achat associées au projet spécifié.
    Chaque commande est représentée par un dictionnaire contenant son id et son po.
    """
    achats = Achat.query.filter_by(projet_id=projet_id).all()
    commandes = [{"id": a.id, "po": a.po} for a in achats]
    current_app.logger.info(f"Commandes pour projet {projet_id}: {commandes}")
    return jsonify(commandes)




# ====================================================
# Route pour afficher les détails d'une commande d'achat (PO)
# ====================================================
@reception_bp.route("/commande/<int:achat_id>", methods=["GET"])
def details_commande(achat_id):
    """
    Affiche les détails de la commande d'achat spécifiée par son ID.
    On affiche la liste des produits commandés, ainsi que les quantités déjà réceptionnées.
    """
    achat = Achat.query.get(achat_id)
    if not achat:
        flash("Commande d'achat introuvée.", "error")
        return redirect(url_for("reception.reception"))
    
    details = []
    for ligne in achat.lignes_achat:
        produit = ligne.produit  # Relation définie dans LigneAchat
        quantite_recue = sum(
            lr.quantite_recue for lr in produit.lignes_reception_detail if lr.reception.achat_id == achat.id
        )
        details.append({
            "produit_id": produit.id,
            "code": produit.code,
            "description": produit.description,
            "quantite_commandee": ligne.quantite,
            "quantite_recue": quantite_recue,
            "quantite_manquante": ligne.quantite - quantite_recue
        })
    return render_template("reception_commande.html", achat=achat, details=details)

@reception_bp.route("/confirmer", methods=["POST"])
def confirmer_reception():
    """
    Confirme la réception pour une commande d'achat.
    Attend les quantités reçues pour chaque produit (avec des clés du type "qte_<produit_id>").
    Met à jour le stock global du produit et l'association avec le projet, puis calcule l'état de la réception (complete ou partielle).
    Retourne une réponse JSON si la requête est AJAX, sinon redirige avec un flash message.
    """
    achat_id = request.form.get("achat_id")
    if not achat_id:
        response = {"message": "Commande d'achat non spécifiée."}
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response), 400
        else:
            flash(response["message"], "error")
            return redirect(url_for("reception.reception"))

    achat = Achat.query.get(achat_id)
    if not achat:
        response = {"message": "Commande d'achat introuvée."}
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response), 404
        else:
            flash(response["message"], "error")
            return redirect(url_for("reception.reception"))

    reception_obj = Reception.query.filter_by(achat_id=achat.id).first()
    if not reception_obj:
        reception_obj = Reception(achat_id=achat.id)
        db.session.add(reception_obj)
        db.session.commit()

    erreurs = []
    from app.models.associations import ProduitProjet

    for ligne in achat.lignes_achat:
        produit = ligne.produit
        input_name = f"qte_{produit.id}"
        qte_str = request.form.get(input_name)
        if qte_str is None:
            continue  # Aucun changement pour ce produit
        try:
            quantite_recue = int(qte_str)
        except ValueError:
            erreurs.append(f"Quantité invalide pour le produit {produit.code}")
            continue

        if quantite_recue < 0:
            erreurs.append(f"Quantité négative pour le produit {produit.code}")
            continue

        # Créer une nouvelle ligne de réception pour ce produit
        nouvelle_ligne = LigneReception(
            reception_id=reception_obj.id,
            produit_id=produit.id,
            quantite_recue=quantite_recue
        )
        db.session.add(nouvelle_ligne)

        # Mise à jour du stock global du produit
        produit.quantite += quantite_recue

        # Mise à jour de l'association ProduitProjet
        association = ProduitProjet.query.filter_by(produit_id=produit.id, projet_id=achat.projet_id).first()
        if association:
            association.quantite += quantite_recue
        else:
            association = ProduitProjet(produit_id=produit.id, projet_id=achat.projet_id, quantite=quantite_recue)
            db.session.add(association)

    if erreurs:
        db.session.rollback()
        response = {"message": "Erreur(s) lors de la confirmation: " + ", ".join(erreurs)}
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response), 400
        else:
            flash(response["message"], "error")
            return redirect(url_for("reception.reception"))

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        response = {"message": f"Erreur lors de la mise à jour: {e}"}
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify(response), 500
        else:
            flash(response["message"], "error")
            return redirect(url_for("reception.reception"))

    # Calcul de l'état de la réception pour l'achat
    etat_reception = "complete"
    for ligne in achat.lignes_achat:
        quantite_recue_total = sum(
            lr.quantite_recue for lr in ligne.produit.lignes_reception_detail if lr.reception.achat_id == achat.id
        )
        if quantite_recue_total < ligne.quantite:
            etat_reception = "partielle"
            break
    reception_obj.etat = etat_reception
    db.session.commit()

    response = {"message": f"Réception confirmée ({etat_reception}). Stocks et associations mis à jour."}
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(response)
    else:
        flash(response["message"], "success")
        return redirect(url_for("reception.reception"))
