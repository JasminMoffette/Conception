from flask import Blueprint, render_template

production_bp = Blueprint('production', __name__)

@production_bp.route("/production")
def production():
    return render_template("production.html")
