import sys
import os

# Ajouter le dossier parent (Conception) au chemin de recherche Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.produit import Produit  # Maintenant, Python peut trouver produit.py



# 1️⃣ Ajouter un produit
produit1 = Produit("P001", "Planche en bois", "Chêne", "Bois", "PO123", "achat", "Entrepôt A", "30x50x2", None, 50, None, "Bois & Co", "Sciage", "CAT-001", "Oui")
produit1.ajouter_produit()

# 2️⃣ Modifier un produit (ex: changer la quantité et l'emplacement)
produit1.modifier_produit(quantite=40, emplacement="Entrepôt B")

# 3️⃣ Récupérer un produit
produit1.recuperer_produit()

# 4️⃣ Supprimer un produit
produit1.supprimer_produit()
