from flask import Blueprint, render_template

reception_bp = Blueprint('reception', __name__)

@reception_bp.route("/")
def reception():
    return render_template("reception.html")

