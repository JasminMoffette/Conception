import os
import pandas as pd
from flask import Flask, render_template, jsonify
import achat
import ajustement
import inventaire
import production
import produit
import reception
import repertoire

# Initialiser l'application Flask
app = Flask(__name__)

# Récupérer le chemin absolu du dossier contenant ce fichier
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "DATA_Plan_entrepot.xlsx")

# Vérifier si le fichier Excel existe avant de le charger
if not os.path.exists(EXCEL_PATH):
    print(f"❌ ERREUR : Le fichier '{EXCEL_PATH}' est introuvable. Assurez-vous qu'il est placé dans {BASE_DIR}.")
    df_plan = None
else:
    df_plan = pd.read_excel(EXCEL_PATH, sheet_name="plan")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/plan")
def plan():
    return render_template("plan.html")

@app.route("/api/emplacements", methods=["GET"])
def get_emplacements():
    if df_plan is None:
        return jsonify({"error": "Fichier Excel introuvable"}), 500

    # Extraire les emplacements
    emplacements = df_plan.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")

    # Extraire les murs
    murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    return jsonify({"emplacements": emplacements, "murs": murs})


# Route pour afficher l'intérieur d'un entrepôt spécifique
@app.route("/entrepot/<nom>")
def afficher_entrepot(nom):
    feuille = nom.lower().replace(" ", "_")  # Adapter pour correspondre au nom de la feuille Excel

    if not os.path.exists(EXCEL_PATH):
        print(f"❌ ERREUR : Impossible d'ouvrir '{EXCEL_PATH}', fichier manquant.")
        return render_template("erreur.html", message="Aucun plan disponible pour cet entrepôt.")

    try:
        df_interieur = pd.read_excel(EXCEL_PATH, sheet_name=feuille)

        # Vérifier que les colonnes existent
        if "Value" in df_interieur and "Position X" in df_interieur and "Position Y" in df_interieur:
            entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
        else:
            entrepot_data = []
            print(f"⚠️ Avertissement : Pas d'objets définis pour {nom}")

        if "Start X" in df_interieur and "Start Y" in df_interieur and "End X" in df_interieur and "End Y" in df_interieur:
            murs_data = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")
        else:
            murs_data = []
            print(f"⚠️ Avertissement : Pas de murs définis pour {nom}")

        return render_template("entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)

    except Exception as e:
        print(f"❌ ERREUR : Impossible de charger la feuille '{feuille}' du fichier Excel ({e})")
        return render_template("erreur.html", message="Aucun plan disponible pour cet entrepôt.")


    
df_murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])

print("✅ Données des murs extraites de l'Excel :")




# Lancer l'application Flask (DOIT ÊTRE À LA FIN)
if __name__ == "__main__":
    print("🚀 Lancement de l'application Flask...")
    app.run(debug=True)

# Tester les fonctionnalités de l'inventaire
print("✅ Test des fonctionnalités de l'inventaire...")
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

