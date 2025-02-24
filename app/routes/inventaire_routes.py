from flask import Blueprint, render_template

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

@inventaire_bp.route("/projet")
def inventaire_projet():
    return render_template("inventaire_projet.html")

@inventaire_bp.route("/quincaillerie")
def quincaillerie():
    return render_template("quincaillerie.html")



