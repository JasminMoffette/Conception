from app import db
from datetime import date

class CommandeProduction(db.Model):
    __tablename__ = 'commandeproduction'
    
    id = db.Column(db.Integer, primary_key=True)
    cp = db.Column(db.String(50), unique=True, nullable=False)
    date_cp = db.Column(db.Date, default=date.today)
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id'), nullable=True)
    commentaire = db.Column(db.Text)

    # Associations
    lignes_commande = db.relationship("LigneCommandeProduction", back_populates="commande_production", cascade="all, delete-orphan")


    def __init__(self, cp, **kwargs):
        self.cp = cp
        self.date_cp = kwargs.get("date_cp", date.today())
        self.projet_id = kwargs.get("projet_id")
        self.commentaire = kwargs.get("commentaire") 


    def __repr__(self):
        return f"<CommandeProduction {self.cp}>"

