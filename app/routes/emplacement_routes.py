from flask import Blueprint, render_template

emplacement_bp = Blueprint('emplacement', __name__)

@emplacement_bp.route("/")
def emplacement():
    return render_template("emplacement.html")

