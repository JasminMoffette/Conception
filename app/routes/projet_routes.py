from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.projet import Projet
from app import db
from datetime import datetime

projet_bp = Blueprint("projet", __name__, url_prefix="/projet")

# ====================================================
# Route principale du module Projet
# ====================================================
@projet_bp.route("/")
def projet():
    """
    Affiche la page principale du module projet.
    """
    return render_template("projet.html")

# ====================================================
# Route pour créer un nouveau projet
# ====================================================
@projet_bp.route("/creer", methods=["POST"])
def creer_projet():
    """
    Crée un nouveau projet à partir des données fournies via le formulaire.
    Les champs requis sont: code, nom, date_creation et responsable.
    Le statut est automatiquement défini à "en cours".
    
    Retourne une réponse JSON en cas de requête Ajax, sinon redirige vers la page principale du module.
    """
    # Récupération des données du formulaire
    code = request.form.get("code")
    nom = request.form.get("nom")
    date_str = request.form.get("date_creation")
    responsable = request.form.get("responsable")
    statut = "en cours"  # Statut par défaut pour un nouveau projet
    
    # Vérification que tous les champs requis sont renseignés
    if not all([code, nom, date_str, responsable]):
        message = "Tous les champs sont requis"
        return {"status": "error", "message": message}
    
    # Conversion de la date
    try:
        date_creation = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        message = "Format de date invalide"
        return {"status": "error", "message": message}
    
    # Création de l'instance Projet
    nouveau_projet = Projet(
        code=code, 
        nom=nom, 
        date_creation=date_creation, 
        responsable=responsable, 
        statut=statut
    )
    
    # Tentative d'enregistrement dans la base de données
    try:
        db.session.add(nouveau_projet)
        db.session.commit()
        message = "Projet créé avec succès"
        status = "success"
    except Exception as e:
        db.session.rollback()
        message = f"Erreur lors de la création du projet : {e}"
        status = "error"
    
    # Si la requête est Ajax, retourner un JSON ; sinon, rediriger avec un flash message
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return {"status": status, "message": message}
    else:
        flash(message, status)
        return redirect(url_for("projet.projet"))

# ====================================================
# Route pour finaliser (mettre à jour le statut) un projet
# ====================================================
@projet_bp.route("/finaliser", methods=["POST"])
def finaliser_projet():
    """
    Met à jour le statut d'un projet.
    Reçoit l'ID du projet et le nouveau statut via le formulaire.
    
    Retourne une réponse JSON pour les requêtes Ajax, sinon redirige vers la page de finalisation.
    """
    project_id = request.form.get("project_id")
    new_status = request.form.get("new_status")
    projet_instance = Projet.query.get(project_id)
    
    if projet_instance:
        projet_instance.statut = new_status
        try:
            db.session.commit()
            message = "Statut mis à jour avec succès"
            status = "success"
        except Exception as e:
            db.session.rollback()
            message = f"Erreur lors de la mise à jour : {e}"
            status = "error"
    else:
        message = "Projet non trouvé"
        status = "error"
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return {"status": status, "message": message}
    else:
        flash(message, status)
        return redirect(url_for("projet.finaliser_data"))

# ====================================================
# Route pour afficher les projets à finaliser
# ====================================================
@projet_bp.route("/finaliser_data")
def finaliser_data():
    """
    Affiche une page listant tous les projets avec le statut "en cours", afin de pouvoir finaliser leur statut.
    """
    projets = Projet.query.filter_by(statut="en cours").all()
    return render_template("finalisation_projet.html", projets=projets)

