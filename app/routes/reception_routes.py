from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, current_app, session
from app.models import Achat, Reception, LigneReception
from app import db
import os

# 📁 Corriger ici le chemin du dossier PDF sur ton système
DOSSIER_PDF = "/Users/mathieumccutcheon/Desktop/Commandes_PO"

reception_bp = Blueprint('reception', __name__)

# ====================================================
# Page principale du module Réception
# ====================================================
@reception_bp.route("/", methods=["GET"])
def reception():
    achats = Achat.query.order_by(Achat.po).all()
    current_app.logger.info(f"Commandes d'achat récupérées pour recherche PO : {len(achats)}")
    return render_template("reception.html", achats=achats)

# ====================================================
# API pour récupérer les commandes d'achat associées à un projet
# ====================================================
@reception_bp.route("/api/commandes/<int:projet_id>", methods=["GET"])
def get_commandes_by_projet(projet_id):
    achats = Achat.query.filter_by(projet_id=projet_id).all()
    commandes = [{"id": a.id, "po": a.po} for a in achats]
    current_app.logger.info(f"Commandes pour projet {projet_id}: {commandes}")
    return jsonify(commandes)

# ====================================================
# Route pour afficher un PDF du bon de commande
# ====================================================
@reception_bp.route("/pdf/<filename>")
def telecharger_pdf(filename):
    return send_from_directory(DOSSIER_PDF, filename)

# ====================================================
# 🔍 Fonction utilitaire pour trouver un PDF correspondant au PO
# ====================================================
def trouver_pdf_par_po(po):
    try:
        fichiers = os.listdir(DOSSIER_PDF)
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'accès au dossier PDF : {e}")
        return None

    for nom in fichiers:
        if nom.endswith(".pdf") and po in nom:
            return nom
    return None

# ====================================================
# Route pour afficher les détails d'une commande d'achat (PO)
# ====================================================
@reception_bp.route("/commande/<int:achat_id>", methods=["GET"])
def details_commande(achat_id):
    achat = Achat.query.get(achat_id)
    if not achat:
        flash("Commande d'achat introuvée.", "error")
        return redirect(url_for("reception.reception"))

    # ✅ Ajout : chercher un PDF correspondant au PO
    nom_pdf = trouver_pdf_par_po(achat.po)

    details = []
    for ligne in achat.lignes_achat:
        produit = ligne.produit
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

    # ✅ Ajout du nom_pdf envoyé à la template
    return render_template("reception_commande.html", achat=achat, details=details, nom_pdf=nom_pdf)

# ====================================================
# Route pour confirmer une réception
# ====================================================
@reception_bp.route("/confirmer", methods=["POST"])
def confirmer_reception():
    achat_id = request.form.get("achat_id")
    if not achat_id:
        flash("Commande d'achat non spécifiée.", "error")
        return redirect(url_for("reception.reception"))

    achat = Achat.query.get(achat_id)
    if not achat:
        flash("Commande d'achat introuvée.", "error")
        return redirect(url_for("reception.reception"))

    reception_obj = Reception.query.filter_by(achat_id=achat.id).first()
    if not reception_obj:
        reception_obj = Reception(achat_id=achat.id)
        db.session.add(reception_obj)
        db.session.commit()

    erreurs = []
    from app.models.associations import ProduitProjet, Stock
    from app.models.emplacement import Emplacement

    for ligne in achat.lignes_achat:
        produit = ligne.produit
        input_name = f"qte_{produit.id}"
        emplacement_name = f"emplacement_{produit.id}"

        qte_str = request.form.get(input_name)
        emplacement_str = request.form.get(emplacement_name)

        if qte_str is None or emplacement_str is None:
            erreurs.append(f"Quantité ou emplacement manquant pour {produit.code}")
            continue

        try:
            quantite_recue = int(qte_str)
        except ValueError:
            erreurs.append(f"Quantité invalide pour le produit {produit.code}")
            continue

        if quantite_recue < 0:
            erreurs.append(f"Quantité négative pour le produit {produit.code}")
            continue

        entrepot, cellule = emplacement_str.split(";")
        emplacement = Emplacement.query.filter_by(entrepot=entrepot, cellule=cellule).first()

        if not emplacement:
            erreurs.append(f"Emplacement introuvable: {emplacement_str} pour le produit {produit.code}")
            continue

        nouvelle_ligne = LigneReception(
            reception_id=reception_obj.id,
            produit_id=produit.id,
            quantite_recue=quantite_recue
        )
        db.session.add(nouvelle_ligne)

        produit.quantite += quantite_recue

        association = ProduitProjet.query.filter_by(produit_id=produit.id, projet_id=achat.projet_id).first()
        if association:
            association.quantite += quantite_recue
        else:
            association = ProduitProjet(produit_id=produit.id, projet_id=achat.projet_id, quantite=quantite_recue)
            db.session.add(association)

        stock_entry = Stock(
            produit_id=produit.id,
            emplacement_id=emplacement.id,
            quantite=quantite_recue,
            achat_id=achat.id
        )
        db.session.add(stock_entry)

    if erreurs:
        db.session.rollback()
        flash("Erreur(s): " + ", ".join(erreurs), "error")
        return redirect(url_for("reception.details_commande", achat_id=achat.id))

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la mise à jour: {e}", "error")
        return redirect(url_for("reception.details_commande", achat_id=achat.id))

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

    flash(f"Réception confirmée ({etat_reception}). Stocks mis à jour.", "success")
    return redirect(url_for("reception.reception"))
