from flask import Blueprint, render_template, jsonify, current_app

emplacement_bp = Blueprint('emplacement', __name__)

@emplacement_bp.route("/")
def emplacement():
    """Affiche la page des emplacements"""
    return render_template("emplacement.html")

@emplacement_bp.route("/api/emplacements", methods=["GET"])
def get_emplacements():
    """Retourne les emplacements et les murs depuis Excel"""
    df_excel = current_app.config.get("df_excel")

    if df_excel is None:
        print("⚠️ ERREUR : df_excel est None. Le fichier Excel n'a pas été chargé correctement.")
        return jsonify({"error": "Fichier Excel introuvable"}), 500

    if "plan" not in df_excel:
        print("⚠️ ERREUR : La feuille 'plan' est absente du fichier Excel.")
        return jsonify({"error": "Feuille 'plan' absente"}), 500

    df_plan = df_excel["plan"]

    # Vérification des colonnes nécessaires avant d'extraire les données
    required_columns_emplacements = {"Value", "Position X", "Position Y"}
    required_columns_murs = {"Start X", "Start Y", "End X", "End Y"}

    if not required_columns_emplacements.issubset(df_plan.columns):
        print(f"⚠️ ERREUR : Colonnes manquantes pour les emplacements : {required_columns_emplacements - set(df_plan.columns)}")
        return jsonify({"error": "Colonnes emplacements manquantes dans le fichier Excel"}), 500

    if not required_columns_murs.issubset(df_plan.columns):
        print(f"⚠️ ERREUR : Colonnes manquantes pour les murs : {required_columns_murs - set(df_plan.columns)}")
        return jsonify({"error": "Colonnes murs manquantes dans le fichier Excel"}), 500

    # Extraire les emplacements et murs du fichier Excel
    emplacements = df_plan.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    print(f"✅ Emplacements récupérés : {len(emplacements)}")
    print(f"✅ Murs récupérés : {len(murs)}")

    return jsonify({"emplacements": emplacements, "murs": murs})

