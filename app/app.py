from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from app.models.achat import Achat  # Importer la classe Achat
from app.models.produit import Produit
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("inventaire.db")  # Remplace "inventaire.db" par le nom de ta base de données si différent
    conn.row_factory = sqlite3.Row  # Permet d’accéder aux résultats sous forme de dictionnaire
    return conn  # Importer la classe Produit

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "achats/"  # Dossier où stocker les fichiers uploadés
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Crée le dossier s'il n'existe pas

# Route pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Route pour la page Achat
@app.route("/achat")
def achat():
    return render_template("achat.html")

# Route pour gérer l'upload de fichier de commande d'achat
@app.route("/upload_commande", methods=['POST'])
def upload_commande():
    if 'file' not in request.files:
        flash("❌ Aucun fichier sélectionné.")
        return redirect(url_for('achat'))

    file = request.files['file']

    if file.filename == '':
        flash("❌ Aucun fichier sélectionné.")
        return redirect(url_for('achat'))

    # Sauvegarde du fichier dans le dossier `achats/`
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Importer la commande et mettre à jour l'inventaire
    achat_module = Achat()
    achat_module.importer_commande(file_path)

    flash(f"✅ Fichier {file.filename} importé et inventaire mis à jour !")
    return redirect(url_for('achat'))

# Route pour la page Ajustement
@app.route("/ajustement")
def ajustement():
    return render_template("ajustement.html")

@app.route("/creer_produit", methods=["POST"])
def creer_produit():
    code = request.form.get("code")

    if not code:
        flash("❌ Le code produit est obligatoire.", "error")
        return redirect(url_for("ajustement"))  # Vérifie bien que ça pointe vers `/ajustement`

    # Vérifier si le produit existe déjà
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produits WHERE code = ?", (code,))
    existing_product = cursor.fetchone()

    if existing_product:
        flash(f"⚠️ Le produit {code} existe déjà dans la base de données.", "warning")
        conn.close()
        return redirect(url_for("ajustement"))

    # Récupérer les attributs sélectionnés
    attributs = {key: request.form.get(key) for key in request.form.keys() if key != "code" and request.form.get(key)}

    # Création du produit avec les attributs sélectionnés
    produit = Produit(code, **attributs)
    produit.ajouter_produit()

    flash(f"✅ Produit {code} ajouté avec succès !", "success")
    return redirect(url_for("ajustement"))



if __name__ == "__main__":
    app.secret_key = "supersecretkey"  # Nécessaire pour les messages flash
    app.run(debug=True)


