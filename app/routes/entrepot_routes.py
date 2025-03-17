from flask import Blueprint, render_template, jsonify, current_app

entrepot_bp = Blueprint('entrepot', __name__)

# ====================================================
# Route pour afficher l'intérieur d'un entrepôt spécifique
# ====================================================
@entrepot_bp.route("/entrepot/<nom>")
def afficher_entrepot(nom):
    """
    Affiche l'intérieur d'un entrepôt spécifique à partir des données extraites du fichier Excel.
    
    Paramètres:
        nom (str): Le nom de l'entrepôt, utilisé pour déterminer le nom de la feuille Excel.
    
    Retour:
        Rendu du template 'entrepot.html' avec les éléments et murs extraits,
        ou une page d'erreur si le fichier ou la feuille est introuvable ou incomplet.
    """
    # Récupérer le DataFrame Excel stocké dans la configuration de l'application
    df_excel = current_app.config.get("df_excel")
    if df_excel is None:
        print(f"⚠️ ERREUR : df_excel est None, impossible d'afficher {nom}")
        return render_template("erreur.html", message="Fichier Excel introuvable."), 500

    # Déterminer le nom de la feuille correspondant à l'entrepôt (conversion en minuscules, espaces remplacés par _)
    feuille = nom.lower().replace(" ", "_")
    print(f"📌 Recherche de la feuille Excel : {feuille}")
    print(f"📄 Feuilles disponibles : {list(df_excel.keys())}")

    if feuille not in df_excel:
        print("⚠️ ERREUR : La feuille Excel n'existe pas !")
        return render_template("erreur.html", message=f"Aucun plan disponible pour l'entrepôt {nom}."), 404

    df_interieur = df_excel[feuille]

    # Définir les colonnes obligatoires pour extraire les éléments et les murs
    required_columns_elements = {"Value", "Position X", "Position Y"}
    required_columns_murs = {"Start X", "Start Y", "End X", "End Y"}

    # Vérifier que les colonnes nécessaires pour les éléments existent
    missing_elements = required_columns_elements - set(df_interieur.columns)
    if missing_elements:
        print(f"⚠️ ERREUR : Colonnes manquantes pour les éléments : {missing_elements}")
        return render_template("erreur.html", message="Colonnes des éléments manquantes dans le fichier Excel."), 500

    # Vérifier que les colonnes nécessaires pour les murs existent
    missing_murs = required_columns_murs - set(df_interieur.columns)
    if missing_murs:
        print(f"⚠️ ERREUR : Colonnes manquantes pour les murs : {missing_murs}")
        return render_template("erreur.html", message="Colonnes des murs manquantes dans le fichier Excel."), 500

    # Extraction des données pour les éléments (emplacements) et les murs
    entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    murs_data = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    print(f"📌 {len(entrepot_data)} éléments et {len(murs_data)} murs chargés.")

    # Rendu du template 'entrepot.html' en passant le nom, les éléments et les murs
    return render_template("entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)
