from flask import Blueprint, render_template, jsonify, current_app, session

emplacement_bp = Blueprint('emplacement', __name__)

# ====================================================
# Route pour afficher la page des emplacements
# ====================================================
@emplacement_bp.route("/")
def emplacement():
    return render_template("plan.html")


# ====================================================
# API pour récupérer les emplacements et les murs depuis le fichier Excel
# ====================================================
@emplacement_bp.route("/api/emplacements", methods=["GET"])
def get_emplacements():
    """
    Retourne les données des emplacements et des murs extraites de la feuille 'plan' du fichier Excel.
    """
    # Récupération du DataFrame Excel stocké dans la configuration
    df_excel = current_app.config.get("df_excel")
    if df_excel is None:
        print("⚠️ ERREUR : df_excel est None. Le fichier Excel n'a pas été chargé correctement.")
        return jsonify({"error": "Fichier Excel introuvable"}), 500

    # Vérifier que la feuille 'plan' est présente
    if "plan" not in df_excel:
        print("⚠️ ERREUR : La feuille 'plan' est absente du fichier Excel.")
        return jsonify({"error": "Feuille 'plan' absente"}), 500

    df_plan = df_excel["plan"]

    # Définir les colonnes requises pour les emplacements et les murs
    required_columns_emplacements = {"Value", "Position X", "Position Y"}
    required_columns_murs = {"Start X", "Start Y", "End X", "End Y"}

    # Vérifier que les colonnes nécessaires sont présentes
    missing_emplacements = required_columns_emplacements - set(df_plan.columns)
    if missing_emplacements:
        print(f"⚠️ ERREUR : Colonnes manquantes pour les emplacements : {missing_emplacements}")
        return jsonify({"error": "Colonnes emplacements manquantes dans le fichier Excel"}), 500

    missing_murs = required_columns_murs - set(df_plan.columns)
    if missing_murs:
        print(f"⚠️ ERREUR : Colonnes manquantes pour les murs : {missing_murs}")
        return jsonify({"error": "Colonnes murs manquantes dans le fichier Excel"}), 500

    # Extraire les enregistrements pour les emplacements et les murs
    emplacements = df_plan.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    print(f"✅ Emplacements récupérés : {len(emplacements)}")
    print(f"✅ Murs récupérés : {len(murs)}")

    return jsonify({"emplacements": emplacements, "murs": murs})


