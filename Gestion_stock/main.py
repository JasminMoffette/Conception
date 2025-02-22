import achat
import ajustement
import inventaire
import production
import produit
import reception
import repertoire
import os
import pandas as pd
from flask import Flask, render_template, jsonify

# Initialiser l'application Flask
app = Flask(__name__)

# Charger le plan global
df_plan = pd.read_excel("DATA_Plan_entrepot.xlsx", sheet_name="plan")

@app.route("/")
def index():
    return render_template("index.html")

# API pour récupérer les emplacements
@app.route("/api/emplacements", methods=["GET"])
def get_emplacements():
    emplacements = df_plan.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    return jsonify(emplacements)

# Route pour afficher l'intérieur d'un entrepôt spécifique
@app.route("/entrepot/<nom>")
def afficher_entrepot(nom):
    try:
        feuille = nom.lower().replace(" ", "_")  # Adapter le nom pour correspondre aux feuilles Excel
        df_interieur = pd.read_excel("DATA_Plan_entrepot.xlsx", sheet_name=feuille)
        entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
        return render_template("entrepot.html", entrepot=nom, elements=entrepot_data)
    except Exception as e:
        print(f"Erreur: {e}")  # Log l'erreur pour debug
        return render_template("erreur.html", message="Aucun plan disponible pour cet entrepôt.")

# Tester les fonctionnalités de l'inventaire (DOIT ÊTRE AVANT `app.run()`)
achat_test = achat.Achat(projet="001")
produits_test = [
    produit.Produit("Ordinateur portable", "OP001", "Électronique", po="PO12345", quantite=5),
    produit.Produit("Souris sans fil", "SS001", "Accessoire", po="PO12345", emplacement="Étagère A", quantite=20),
    produit.Produit("Écran 24 pouces", "EC001", "Électronique", po="PO12346", dimension="24x18x2", quantite=10),
    produit.Produit("Clavier mécanique", "CM001", "Accessoire", po="PO12347", emplacement="Étagère B", dimension="18x6x1", quantite=15),
    produit.Produit("Câble HDMI", "CH001", "Accessoire", po="PO12348", quantite=50)
]

inventaire_test = inventaire.Inventaire("001")
for i in produits_test:
    inventaire_test.ajouter_produit(i)

repertoire_test = repertoire.Repertoire()
repertoire_test.ajouter_inventaire(inventaire_test)

print(inventaire_test.produits)
print(produits_test[0])
print(produits_test)
print(repertoire_test.inventaires)
print(inventaire_test)

# Lancer l'application Flask (DOIT ÊTRE À LA FIN)
if __name__ == "__main__":
    app.run(debug=True)
