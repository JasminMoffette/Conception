import os
import pandas as pd
from app.models.produit import Produit
from app import db

class Achat:
    def __init__(self, dossier_achats="achats/"):
        """ Initialise le module Achat et crée un dossier pour les fichiers de commande. """
        self.dossier_achats = dossier_achats
        os.makedirs(self.dossier_achats, exist_ok=True)

    def importer_commande(self, fichier_path):
        """Importe un fichier de commande (Excel ou CSV) et met à jour l'inventaire."""
        if not os.path.exists(fichier_path):
            print(f"❌ Le fichier {fichier_path} n'existe pas.")
            return

        if fichier_path.endswith(".csv"):
            df = pd.read_csv(fichier_path)
        elif fichier_path.endswith(".xlsx"):
            df = pd.read_excel(fichier_path)
        else:
            print("❌ Format de fichier non supporté.")
            return

        for _, row in df.iterrows():
            code = row.get("code")
            description = row.get("description", "")
            quantite = row.get("quantite", 0)
            emplacement = row.get("emplacement", "")

            if not code:
                print("⚠️ Ligne ignorée (code produit manquant).")
                continue

            produit_existant = Produit.query.filter_by(code=code).first()

            if produit_existant:
                # Produit existe déjà : mise à jour quantité
                produit_existant.quantite += quantite
                db.session.commit()
                print(f"🔄 Produit {code} mis à jour : nouvelle quantité = {produit_existant.quantite}")
            else:
                # Si le produit n'existe pas, on le crée
                nouveau_produit = Produit(
                    code=code,
                    description=description,
                    quantite=quantite,
                    emplacement=emplacement
                )
                db.session.add(nouveau_produit)
                db.session.commit()
                print(f"✅ Nouveau produit {code} ajouté avec quantité = {quantite}")

        print("🎯 Mise à jour de l'inventaire terminée !")
