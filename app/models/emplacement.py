from app import db

class Emplacement(db.Model):
    __tablename__ = 'emplacement'
    
    id = db.Column(db.Integer, primary_key=True)
    entrepot = db.Column(db.String(100), nullable=False)
    cellule = db.Column(db.String(100), nullable=False)

    # Relation avec Stock, qui permet de suivre les produits stockés dans cet emplacement
    stocks = db.relationship("Stock", back_populates="emplacement", cascade="all, delete-orphan")


    def __init__(self, entrepot, cellule, **kwargs):
        self.entrepot = entrepot
        self.cellule = cellule
        # Affecte les autres attributs éventuels passés en kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<Emplacement {self.entrepot} - {self.cellule}>"

    def ajouter_emplacement(self):
        """Ajoute cet emplacement à la base de données."""
        db.session.add(self)
        db.session.commit()
        print(f"✅ Emplacement {self.entrepot} - {self.cellule} ajouté avec succès.")

    def modifier_emplacement(self, **kwargs):
        """Modifie les attributs de cet emplacement et sauvegarde les modifications."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Emplacement {self.entrepot} - {self.cellule} mis à jour avec succès.")

    @classmethod
    def recuperer_emplacement(cls, entrepot, cellule):
        """Retourne l'emplacement correspondant à l'entrepôt et la cellule donnés, ou None si non trouvé."""
        return cls.query.filter_by(entrepot=entrepot, cellule=cellule).first()

    def supprimer_emplacement(self):
        """Supprime cet emplacement de la base de données."""
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Emplacement {self.entrepot} - {self.cellule} supprimé avec succès.")

