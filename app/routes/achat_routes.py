from flask import Blueprint, render_template

achat_bp = Blueprint('achat', __name__)

@achat_bp.route("/")
def achat():
    return render_template("achat.html")

