import pandas as pd
import os
from app.models.produit import Produit

class Achat:
    def __init__(self, dossier_achats="achats/"):
        """ Initialise le module Achat et crée un dossier pour les fichiers de commande. """
        self.dossier_achats = dossier_achats
        os.makedirs(self.dossier_achats, exist_ok=True)  # Crée le dossier s'il n'existe pas

    def importer_commande(self, fichier_path):
        """ Lit un fichier de commande d'achat (Excel ou CSV) et met à jour l'inventaire. """
        if not os.path.exists(fichier_path):
            print(f"❌ Le fichier {fichier_path} n'existe pas.")
            return
        
        # Déterminer si c'est un fichier CSV ou Excel
        if fichier_path.endswith(".csv"):
            df = pd.read_csv(fichier_path)
        elif fichier_path.endswith(".xlsx") or fichier_path.endswith(".xls"):
            df = pd.read_excel(fichier_path)
        else:
            print("❌ Format de fichier non supporté. Utilisez CSV ou Excel.")
            return
        
        print(f"📂 Lecture du fichier {fichier_path}...")

        for _, row in df.iterrows():
            code = row.get("code", None)
            description = row.get("description", None)
            quantite = row.get("quantite", 0)
            emplacement = row.get("emplacement", None)

            if not code:
                print("⚠️ Ligne ignorée (code produit manquant).")
                continue
            
            # Vérifier si le produit existe déjà
            produit = Produit(code)
            produit_existant = produit.recuperer_produit()

            if produit_existant:
                # Si le produit existe, on met à jour la quantité
                quantite_actuelle = produit_existant[8]  # La colonne "quantite" est à l'index 8
                nouvelle_quantite = quantite_actuelle + quantite
                produit.modifier_produit(quantite=nouvelle_quantite)
                print(f"🔄 Produit {code} mis à jour : {quantite_actuelle} ➝ {nouvelle_quantite}")
            else:
                # Si le produit n'existe pas, on l'ajoute
                nouveau_produit = Produit(code, description, quantite, emplacement)
                nouveau_produit.ajouter_produit()
                print(f"✅ Nouveau produit {code} ajouté avec {quantite} unités.")

        print("🎯 Mise à jour de l'inventaire terminée !")
