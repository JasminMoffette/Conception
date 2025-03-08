from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from app.models.achat import Achat  

achat_bp = Blueprint('achat_bp', __name__)

@achat_bp.route("/")
def achat():
    """Affiche clairement la page d'achat."""
    return render_template("achat.html")

@achat_bp.route("/upload_commande", methods=['POST'])
def upload_commande():
    """Gère proprement l'upload d'un fichier commande."""
    if 'file' not in request.files:
        flash("❌ Aucun fichier sélectionné.", "error")
        return redirect(url_for('achat_bp.achat'))

    file = request.files['file']

    if file.filename == '':
        flash("❌ Aucun fichier sélectionné.", "error")
        return redirect(url_for('achat_bp.achat'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)


    achat_module = Achat()
    achat_module.importer_commande(file_path)

    flash(f"✅ Fichier {file.filename} importé et inventaire mis à jour !", "success")
    return redirect(url_for('achat_bp.achat'))



