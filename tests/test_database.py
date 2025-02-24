import sys
import os

# Ajoute le dossier parent (Conception) au chemin de recherche Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Database  # Maintenant, Python peut trouver app/


# Test de la base de données
db = Database()
print("✅ Base de données 'inventaire.db' et table 'produits' créées avec succès.")
db.fermer_connexion()



