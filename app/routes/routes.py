from flask import render_template, jsonify

def setup_routes(app, df_excel):
    """ Configuration de toutes les routes Flask. """

    # Page d'accueil
    app.add_url_rule("/", "index", lambda: render_template("index.html"))

    # Page du plan
    app.add_url_rule("/plan", "plan", lambda: render_template("plan.html"))

    # API pour récupérer les emplacements et murs
    @app.route("/api/emplacements", methods=["GET"])
    def get_emplacements():
        if df_excel is None or "plan" not in df_excel:
            return jsonify({"error": "Fichier Excel introuvable"}), 500
        
        df_plan = df_excel["plan"]
        emplacements = df_plan.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records")
        murs = df_plan.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records")

        return jsonify({"emplacements": emplacements, "murs": murs})

    # Route pour afficher l'intérieur d'un entrepôt spécifique
    @app.route("/entrepot/<nom>")
    def afficher_entrepot(nom):
        feuille = nom.lower().replace(" ", "_")

        if df_excel is None or feuille not in df_excel:
            return render_template("erreur.html", message="Aucun plan disponible pour cet entrepôt.")

        df_interieur = df_excel[feuille]
        entrepot_data = df_interieur.dropna(subset=["Value", "Position X", "Position Y"])[["Value", "Position X", "Position Y"]].to_dict(orient="records") if "Value" in df_interieur else []
        murs_data = df_interieur.dropna(subset=["Start X", "Start Y", "End X", "End Y"])[["Start X", "Start Y", "End X", "End Y"]].to_dict(orient="records") if "Start X" in df_interieur else []

        return render_template("entrepot.html", entrepot=nom, elements=entrepot_data, murs=murs_data)
    
    @app.route("/inventaire/general")
    def inventaire_general():
        return render_template("inventaire_general.html")

    @app.route("/inventaire/libre")
    def inventaire_libre():
        return render_template("inventaire_libre.html")

    @app.route("/inventaire/projet")
    def inventaire_projet():
        return render_template("inventaire_projet.html")

    @app.route("/inventaire/quincaillerie")
    def quincaillerie():
        return render_template("quincaillerie.html")


    # Routes dynamiques pour les modules de gestion (achat, réception, etc.)
    def render_dynamic_module(module_name):
        return render_template(f"{module_name}.html")

    modules = ["achat", "reception", "inventaire", "production", "ajustement"]
    for module in modules:
        app.add_url_rule(f"/{module}", module, render_dynamic_module, defaults={"module_name": module})

    # 🔍 Vérification : Afficher toutes les routes enregistrées
    #print("\n📌 Routes enregistrées dans Flask :")
    #for rule in app.url_map.iter_rules():
       # print(f"{rule} → {rule.endpoint}")

        
        

