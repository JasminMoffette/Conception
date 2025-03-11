from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.projet import Projet
from app import db

projet_bp = Blueprint("projet", __name__, url_prefix="/projet")

@projet_bp.route("/")
def projet():
    return render_template("projet.html")

@projet_bp.route("/creer", methods=["POST"])
def creer_projet():
    code = request.form.get("code")
    nom = request.form.get("nom")
    date_str = request.form.get("date_creation")
    responsable = request.form.get("responsable")
    statut = "en cours"  # Définir le statut automatiquement
    
    if not all([code, nom, date_str, responsable]):
        message = "Tous les champs sont requis"
        return {"status": "error", "message": message}
    
    from datetime import datetime
    try:
        date_creation = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        message = "Format de date invalide"
        return {"status": "error", "message": message}
    
    nouveau_projet = Projet(code=code, nom=nom, date_creation=date_creation, responsable=responsable, statut=statut)
    
    try:
        db.session.add(nouveau_projet)
        db.session.commit()
        message = "Projet créé avec succès"
        status = "success"
    except Exception as e:
        db.session.rollback()
        message = f"Erreur lors de la création du projet : {e}"
        status = "error"
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return {"status": status, "message": message}
    else:
        flash(message, status)
        return redirect(url_for("projet.projet"))





@projet_bp.route("/finaliser", methods=["POST"])
def finaliser_projet():
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
    
@projet_bp.route("/finaliser_data")
def finaliser_data():
    projets = Projet.query.filter_by(statut="en cours").all()
    return render_template("finalisation_projet.html", projets=projets)





