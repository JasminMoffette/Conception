from app import db
from datetime import datetime

class CommandeProduction(db.Model):
    __tablename__ = 'commandeproduction'
    id = db.Column(db.Integer, primary_key=True)
    cp = db.Column(db.String(50), unique=True, nullable=False)
    date_cp = db.Column(db.DateTime, default=datetime.utcnow)
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id'), nullable=True)  # Lien vers Projet

    lignes_commande = db.relationship("LigneCommandeProduction", back_populates="commande_production", cascade="all, delete-orphan")

    def __init__(self, cp, **kwargs):
        self.cp = cp
        self.date_cp = kwargs.get("date_cp", datetime.utcnow())
        self.projet_id = kwargs.get("projet_id")
        for key, value in kwargs.items():
            setattr(self, key, value)

    def ajouter_commande(self):
        db.session.add(self)
        db.session.commit()
        print(f"✅ CommandeProduction {self.cp} ajoutée avec succès.")

    def modifier_commande(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ CommandeProduction {self.cp} mise à jour avec succès.")

    @classmethod
    def recuperer_commande(cls, cp):
        return cls.query.filter_by(cp=cp).first()

    def supprimer_commande(self):
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ CommandeProduction {self.cp} supprimée avec succès.")
