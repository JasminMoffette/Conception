from flask import Blueprint, render_template

production_bp = Blueprint('production', __name__)  # ✅ Vérifie bien le nom ici

@production_bp.route("/")  # ✅ Assure-toi que la route est correcte
def production():
    return render_template("production.html")



