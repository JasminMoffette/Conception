import os
import pandas as pd
from app.models.produit import Produit
from app.models.achat import Achat
from app import db

class AchatImporter:
    def __init__(self, dossier_achats="achats/"):
        """
        Initialise le module d'importation des achats et crée un dossier pour les fichiers de commande.
        """
        self.dossier_achats = dossier_achats
        os.makedirs(self.dossier_achats, exist_ok=True)

    def importer_commande(self, fichier_path):
        """
        Importe un fichier de commande (Excel ou CSV) et met à jour l'inventaire.

        Paramètres:
            fichier_path (str): Chemin vers le fichier de commande.
        """
        if not os.path.exists(fichier_path):
            print(f"❌ Le fichier {fichier_path} n'existe pas.")
            return

        # Charger le fichier en fonction de son extension
        if fichier_path.endswith(".csv"):
            df = pd.read_csv(fichier_path)
        elif fichier_path.endswith(".xlsx"):
            df = pd.read_excel(fichier_path)
        else:
            print("❌ Format de fichier non supporté.")
            return

        # Parcours de chaque ligne du DataFrame
        for _, row in df.iterrows():
            po = row.get("po")
            code = row.get("code")
            description = row.get("description", "")
            quantite = row.get("quantite", 0)
            fournisseur = row.get("fournisseur", "")
            prix = row.get("prix", 0.0)

            if not code:
                print("⚠️ Ligne ignorée (code produit manquant).")
                continue

            # Mise à jour ou création du produit
            produit_existant = Produit.query.filter_by(code=code).first()
            if produit_existant:
                produit_existant.quantite += quantite
                db.session.commit()
                print(f"🔄 Produit {code} mis à jour : nouvelle quantité = {produit_existant.quantite}")
            else:
                nouveau_produit = Produit(
                    code=code,
                    description=description,
                    quantite=quantite
                )
                db.session.add(nouveau_produit)
                db.session.commit()
                print(f"✅ Nouveau produit {code} ajouté avec quantité = {quantite}")

            # Gérer l'achat s'il est spécifié
            if po:
                achat_existant = Achat.recuperer_achat(po)
                if not achat_existant:
                    nouvel_achat = Achat(
                        po=po,
                        fournisseur=fournisseur,
                        prix=prix
                    )
                    db.session.add(nouvel_achat)
                    db.session.commit()
                    print(f"✅ Achat {po} ajouté avec succès.")
                else:
                    print(f"⚠️ Achat {po} existe déjà, aucune action effectuée.")

        print("🎯 Mise à jour de l'inventaire terminée !")
