from app.database import Database

class Projet:
    def __init__(self, nom):
        """Initialise un projet."""
        self.nom = nom
        self.db = Database()

    def ajouter_projet(self):
        """Ajoute un projet à la base de données s'il n'existe pas déjà."""
        self.db.cursor.execute("SELECT * FROM projet_produits WHERE projet = ?", (self.nom,))
        existing_project = self.db.cursor.fetchone()
        
        if existing_project:
            print(f"⚠️ Le projet '{self.nom}' existe déjà.")
        else:
            self.db.cursor.execute("INSERT INTO projet_produits (projet) VALUES (?)", (self.nom,))
            self.db.conn.commit()
            print(f"✅ Projet '{self.nom}' ajouté avec succès.")

    def attribuer_produit(self, code_produit, quantite):
        """Associe un produit à ce projet avec une certaine quantité."""
        # Vérifier la quantité disponible
        self.db.cursor.execute("SELECT quantite FROM produits WHERE code = ?", (code_produit,))
        result = self.db.cursor.fetchone()
        
        if result is None:
            print(f"❌ Erreur : Produit '{code_produit}' introuvable.")
            return False
        
        quantite_disponible = result[0]

        if quantite > quantite_disponible:
            print(f"❌ Erreur : Quantité demandée ({quantite}) supérieure à la quantité disponible ({quantite_disponible}).")
            return False

        # Ajouter le produit au projet et mettre à jour la quantité disponible
        self.db.cursor.execute(
            "INSERT INTO projet_produits (code_produit, projet, quantite) VALUES (?, ?, ?)",
            (code_produit, self.nom, quantite)
        )
        nouvelle_quantite = quantite_disponible - quantite
        self.db.cursor.execute("UPDATE produits SET quantite = ? WHERE code = ?", (nouvelle_quantite, code_produit))
        self.db.conn.commit()

        print(f"✅ {quantite} unités du produit '{code_produit}' attribuées au projet '{self.nom}'.")
        return True

    def obtenir_produits(self):
        """Récupère les produits associés à ce projet."""
        self.db.cursor.execute(
            "SELECT p.code, p.description, pp.quantite FROM projet_produits pp "
            "JOIN produits p ON pp.code_produit = p.code WHERE pp.projet = ?", (self.nom,)
        )
        return self.db.cursor.fetchall()

    def supprimer_projet(self):
        """Supprime le projet et ses associations de la base de données."""
        self.db.cursor.execute("DELETE FROM projet_produits WHERE projet = ?", (self.nom,))
        self.db.conn.commit()
        print(f"🗑️ Projet '{self.nom}' supprimé avec succès.")
