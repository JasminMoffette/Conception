from app import db
from datetime import date

class Achat(db.Model):
    __tablename__ = 'achat'
    
    id = db.Column(db.Integer, primary_key=True)
    po = db.Column(db.String(50), unique=True, nullable=False)
    date_achat = db.Column(db.Date, default=date.today)
    fournisseur = db.Column(db.String(100))
    prix = db.Column(db.Float)
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id'), nullable=True)

    # Associations
    lignes_achat = db.relationship("LigneAchat", back_populates="achat", cascade="all, delete-orphan")

    def __init__(self, po, **kwargs):
        self.po = po
        self.date_achat = kwargs.get("date_achat", date.today())
        self.fournisseur = kwargs.get("fournisseur")
        self.prix = kwargs.get("prix", 0.0)
        self.projet_id = kwargs.get("projet_id")

    def __repr__(self):
        return f"<Achat {self.po}>"




