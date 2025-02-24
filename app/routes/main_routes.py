from flask import Blueprint, render_template, jsonify, current_app

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    """ Affiche la page d'accueil """
    return render_template("index.html")

@main_bp.route("/plan")
def plan():
    """ Affiche la page du plan de l'usine """
    return render_template("plan.html")

@main_bp.route("/api/emplacements", methods=["GET"])
def get_emplacements():
    """ Retourne les emplacements et les murs depuis Excel """
    df_excel = current_app.config.get("df_excel")

    if df_excel is None:
        print("⚠️ Alerte : df_excel est None, le fichier Excel n'a pas été chargé correctement.")
        return jsonify({"error": "Fichier Excel introuvable"}), 500

    if "plan" not in df_excel:
        print("⚠️ Alerte : La feuille 'plan' est absente dans le fichier Excel.")
        return jsonify({"error": "Feuille 'plan' introuvable dans Excel"}), 500

    df_plan = df_excel["plan"]
    emplacements = df_plan.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
    murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

    return jsonify({"emplacements": emplacements, "murs": murs})


