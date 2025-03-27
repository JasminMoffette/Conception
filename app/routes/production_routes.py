from flask import Blueprint, render_template, session

production_bp = Blueprint('production', __name__)

@production_bp.route("/")
def production():
    """
    Affiche la page principale du module Production.
    (À développer ultérieurement.)
    """
    return render_template("production.html")




