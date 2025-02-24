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

    if df_excel is None or "plan" not in df_excel:
        return jsonify({"error": "Fichier Excel introuvable ou feuille 'plan' absente"}), 500

    df_plan = df_excel["plan"]
    
    # Extraire les emplacements et murs du fichier Excel
    emplacements = df_plan.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    return jsonify({"emplacements": emplacements, "murs": murs})

