from app import db

class Emplacement(db.Model):
    __tablename__ = 'emplacement'
    id = db.Column(db.Integer, primary_key=True)
    entrepot = db.Column(db.String(100), nullable=False)
    cellule = db.Column(db.String(100), nullable=False)

    stocks = db.relationship("Stock", back_populates="emplacement", cascade="all, delete-orphan")


    def __init__(self, entrepot, cellule, **kwargs):
        self.entrepot = entrepot
        self.cellule = cellule
        for key, value in kwargs.items():
            setattr(self, key, value)

    def ajouter_emplacement(self):
        db.session.add(self)
        db.session.commit()
        print(f"✅ Emplacement {self.entrepot} - {self.cellule} ajouté avec succès.")

    def modifier_emplacement(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Emplacement {self.entrepot} - {self.cellule} mis à jour avec succès.")

    @classmethod
    def recuperer_emplacement(cls, entrepot, cellule):
        return cls.query.filter_by(entrepot=entrepot, cellule=cellule).first()

    def supprimer_emplacement(self):
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Emplacement {self.entrepot} - {self.cellule} supprimé avec succès.")
