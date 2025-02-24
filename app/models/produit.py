from app.database import Database
import json  # Pour gérer l'historique sous forme de liste

class Produit:
    def __init__(self, code, description=None, materiaux=None, categorie=None, po=None, statut=None, emplacement=None, dimension=None, projet=None, quantite=0, cp=None, fournisseur=None, coupe=None, no_catalogue=None, fsc=None, historique=None):
        """ Initialise un produit de l'inventaire. """
        self.code = code
        self.description = description
        self.materiaux = materiaux
        self.categorie = categorie
        self.po = po
        self.statut = statut
        self.emplacement = emplacement
        self.dimension = dimension
        self.projet = projet
        self.quantite = quantite
        self.cp = cp
        self.fournisseur = fournisseur
        self.coupe = coupe
        self.no_catalogue = no_catalogue
        self.fsc = fsc
        self.historique = historique if historique is not None else []
        self.db = Database()  # Connexion à la base de données

    def ajouter_produit(self):

        historique_str = json.dumps(self.historique) if isinstance(self.historique, list) else self.historique
        """Ajoute un produit à la base de données s'il n'existe pas déjà."""
        self.db.cursor.execute("SELECT * FROM produits WHERE code = ?", (self.code,))
        existing_product = self.db.cursor.fetchone()

        if existing_product:
            print(f"⚠️ Le produit {self.code} existe déjà.")
        else:
            self.db.cursor.execute("""
                INSERT INTO produits (code, description, materiaux, categorie, po, statut, emplacement, dimension, projet, quantite, cp, fournisseur, coupe, no_catalogue, fsc, historique)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.code, self.description, self.materiaux, self.categorie, self.po, self.statut, self.emplacement,
                  self.dimension, self.projet, self.quantite, self.cp, self.fournisseur, self.coupe,
                  self.no_catalogue, self.fsc, json.dumps(self.historique)))
            self.db.conn.commit()
            print(f"✅ Produit {self.code} ajouté avec succès !")

    def modifier_produit(self, **kwargs):
        """Modifie les attributs d'un produit existant sans écraser les autres champs."""
        updates = ", ".join([f"{key} = ?" for key in kwargs])
        values = list(kwargs.values()) + [self.code]

        self.db.cursor.execute(f"UPDATE produits SET {updates} WHERE code = ?", values)
        self.db.conn.commit()
        print(f"✅ Produit {self.code} mis à jour avec succès.")

    def recuperer_produit(self):
        """Récupère un produit depuis la base de données."""
        self.db.cursor.execute("SELECT * FROM produits WHERE code = ?", (self.code,))
        produit = self.db.cursor.fetchone()

        if produit:
            print(f"ℹ️ Détails du produit {self.code}: {produit}")
            return produit
        else:
            print(f"❌ Produit {self.code} non trouvé.")
            return None

    def supprimer_produit(self):
        """Supprime un produit de la base de données."""
        self.db.cursor.execute("DELETE FROM produits WHERE code = ?", (self.code,))
        self.db.conn.commit()
        print(f"🗑️ Produit {self.code} supprimé avec succès.")



