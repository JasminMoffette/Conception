from flask import Blueprint, render_template

ajustement_bp = Blueprint('ajustement', __name__)

@ajustement_bp.route("/")
def ajustement():
    return render_template("ajustement.html")

