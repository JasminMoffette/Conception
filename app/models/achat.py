from app import db
from datetime import datetime

class Achat(db.Model):
    __tablename__ = 'achat'
    id = db.Column(db.Integer, primary_key=True)
    po = db.Column(db.String(50), unique=True, nullable=False)
    date_achat = db.Column(db.DateTime, default=datetime.utcnow)
    fournisseur = db.Column(db.String(100))
    prix = db.Column(db.Float)
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id'), nullable=True)

    # Relation avec LigneAchat
    lignes_achat = db.relationship("LigneAchat", back_populates="achat", cascade="all, delete-orphan")

    def __init__(self, po, **kwargs):
        self.po = po
        self.date_achat = kwargs.get("date_achat", datetime.utcnow())
        self.fournisseur = kwargs.get("fournisseur")
        self.prix = kwargs.get("prix", 0.0)
        self.projet_id = kwargs.get("projet_id")

    def ajouter_achat(self):
        db.session.add(self)
        db.session.commit()
        print(f"✅ Achat {self.po} ajouté avec succès.")

    def modifier_achat(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Achat {self.po} mis à jour avec succès.")

    @classmethod
    def recuperer_achat(cls, po):
        return cls.query.filter_by(po=po).first()

    def supprimer_achat(self):
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Achat {self.po} supprimé avec succès.")
