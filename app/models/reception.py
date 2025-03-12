from app import db
from datetime import datetime

class Reception(db.Model):
    __tablename__ = 'reception'
    
    id = db.Column(db.Integer, primary_key=True)
    date_reception = db.Column(db.DateTime, default=datetime.utcnow)
    # Clé étrangère vers Achat pour indiquer à quelle commande cette réception correspond
    achat_id = db.Column(db.Integer, db.ForeignKey('achat.id'), nullable=False)

    # Relation pour accéder aux lignes de réception associées
    lignes_reception = db.relationship("LigneReception", back_populates="reception", cascade="all, delete-orphan")

    def __init__(self, achat_id, **kwargs):
        self.achat_id = achat_id
        self.date_reception = kwargs.get("date_reception", datetime.utcnow())

    def __repr__(self):
        return f"<Reception Achat {self.achat_id} - ID {self.id}>"

    def ajouter_reception(self):
        db.session.add(self)
        db.session.commit()
        print(f"✅ Réception pour Achat {self.achat_id} ajoutée avec succès.")

    def modifier_reception(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Réception {self.id} mise à jour avec succès.")

    def supprimer_reception(self):
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Réception {self.id} supprimée avec succès.")
