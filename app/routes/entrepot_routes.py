from flask import Blueprint, render_template, jsonify, current_app

entrepot_bp = Blueprint('entrepot', __name__)

@entrepot_bp.route("/entrepot/<nom>")
def afficher_entrepot(nom):
    """Affiche l'intérieur d'un entrepôt spécifique"""
    df_excel = current_app.config.get("df_excel")

    if df_excel is None:
        print(f"⚠️ Erreur : df_excel est None, impossible d'afficher {nom}")
        return render_template("erreur.html", message="Fichier Excel introuvable."), 500

    # Vérifier si l'entrepôt existe dans les feuilles Excel
    feuille = nom.lower().replace(" ", "_")
    print(f"📌 Recherche de la feuille Excel : {feuille}")

    if feuille not in df_excel:
        print("⚠️ Erreur : La feuille Excel n'existe pas !")
        return render_template("erreur.html", message=f"Aucun plan disponible pour l'entrepôt {nom}."), 404

    df_interieur = df_excel[feuille]
    
    entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records") if "Value" in df_interieur else []
    murs_data = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records") if "Start X" in df_interieur else []

    print(f"📌 {len(entrepot_data)} éléments et {len(murs_data)} murs chargés.")

    return render_template("entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)
