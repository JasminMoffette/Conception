from flask import Flask, render_template, jsonify
import inventaire  # Importez ici vos modules existants
import produit


app = Flask(__name__)

# Route pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Exemple de route API pour récupérer l'inventaire
@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    # Ici, vous pouvez utiliser vos fonctions existantes pour récupérer les données
    # Pour l'instant, nous utilisons des données statiques d'exemple
    inventory = [
        {"name": "Ordinateur portable", "code": "OP001", "quantity": 5},
        {"name": "Souris sans fil", "code": "SS001", "quantity": 20},
        {"name": "Écran 24 pouces", "code": "EC001", "quantity": 10},
        {"name": "Clavier mécanique", "code": "CM001", "quantity": 15},
        {"name": "Câble HDMI", "code": "CH001", "quantity": 50}
    ]
    return jsonify(inventory)

if __name__ == "__main__":
    app.run(debug=True)
