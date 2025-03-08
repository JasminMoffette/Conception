from flask import Blueprint, render_template, jsonify, current_app

entrepot_bp = Blueprint('entrepot', __name__)

@entrepot_bp.route("/entrepot/<nom>")
def afficher_entrepot(nom):
    """Affiche l'intérieur d'un entrepôt spécifique à partir du fichier Excel."""
    df_excel = current_app.config.get("df_excel")

    if df_excel is None:
        print(f"⚠️ ERREUR : df_excel est None, impossible d'afficher {nom}")
        return render_template("erreur.html", message="Fichier Excel introuvable."), 500

    # Vérifier si l'entrepôt existe dans les feuilles Excel
    feuille = nom.lower().replace(" ", "_")
    print(f"📌 Recherche de la feuille Excel : {feuille}")
    print(f"📄 Feuilles disponibles : {list(df_excel.keys())}")  # Debugging

    if feuille not in df_excel:
        print("⚠️ ERREUR : La feuille Excel n'existe pas !")
        return render_template("erreur.html", message=f"Aucun plan disponible pour l'entrepôt {nom}."), 404

    df_interieur = df_excel[feuille]

    # Vérification des colonnes obligatoires avant extraction des données
    required_columns_elements = {"Value", "Position X", "Position Y"}
    required_columns_murs = {"Start X", "Start Y", "End X", "End Y"}

    if not required_columns_elements.issubset(df_interieur.columns):
        print(f"⚠️ ERREUR : Colonnes manquantes pour les éléments : {required_columns_elements - set(df_interieur.columns)}")
        return render_template("erreur.html", message="Colonnes des éléments manquantes dans le fichier Excel."), 500

    if not required_columns_murs.issubset(df_interieur.columns):
        print(f"⚠️ ERREUR : Colonnes manquantes pour les murs : {required_columns_murs - set(df_interieur.columns)}")
        return render_template("erreur.html", message="Colonnes des murs manquantes dans le fichier Excel."), 500

    # Extraction des données
    entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    murs_data = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    print(f"📌 {len(entrepot_data)} éléments et {len(murs_data)} murs chargés.")

    return render_template("entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)

