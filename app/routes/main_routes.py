from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/plan")
def plan():
    return render_template("plan.html")

@main_bp.route("/entrepot/<nom>")
def afficher_entrepot(nom):
    feuille = nom.lower().replace(" ", "_")

    if "df_excel" not in globals() or df_excel is None or feuille not in df_excel:
        return render_template("erreur.html", message="Aucun plan disponible pour cet entrepôt.")

    df_interieur = df_excel[feuille]
    entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records") if "Value" in df_interieur else []
    murs_data = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records") if "Start X" in df_interieur else []

    return render_template("entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)

