
from flask import render_template, jsonify

def setup_routes(app, df_excel):
    """ Configuration de toutes les routes Flask. """

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/plan")
    def plan():
        return render_template("plan.html")

    @app.route("/api/emplacements", methods=["GET"])
    def get_emplacements():
        if df_excel is None or "plan" not in df_excel:
            return jsonify({"error": "Fichier Excel introuvable"}), 500
        
        df_plan = df_excel["plan"]

        emplacements = df_plan.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
        murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

        return jsonify({"emplacements": emplacements, "murs": murs})

    @app.route("/entrepot/<nom>")
    def afficher_entrepot(nom):
        """ Afficher l'intérieur d'un entrepôt spécifique. """
        feuille = nom.lower().replace(" ", "_")

        if df_excel is None or feuille not in df_excel:
            return render_template("erreur.html", message="Aucun plan disponible pour cet entrepôt.")

        df_interieur = df_excel[feuille]

        entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records") if "Value" in df_interieur else []
        murs_data = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records") if "Start X" in df_interieur else []

        return render_template("entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)

    # Routes pour les modules de gestion (Achat, Réception, etc.)
    def render_module(module):
        return render_template(f"{module}.html")

    modules = ["achat", "reception", "inventaire", "production", "ajustement"]
    for module in modules:
        app.add_url_rule(f"/{module}", module, lambda module_name=module: render_module(module_name))

