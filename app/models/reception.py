from app import db
from datetime import date

class Reception(db.Model):
    __tablename__ = 'reception'
    
    id = db.Column(db.Integer, primary_key=True)
    date_reception = db.Column(db.Date)
    achat_id = db.Column(db.Integer, db.ForeignKey('achat.id'), nullable=False)
    etat = db.Column(db.String(20), default="en attente")
    commentaire = db.Column(db.Text)

    # Associasions
    lignes_reception = db.relationship("LigneReception", back_populates="reception", cascade="all, delete-orphan")


    def __init__(self, achat_id, **kwargs):
        self.achat_id = achat_id
        self.date_reception = kwargs.get("date_reception")
        self.etat = kwargs.get("etat", "en attente")
        self.commentaire = kwargs.get("commentaire")

    def __repr__(self):
       return f"<Reception Achat {self.achat_id} - ID {self.id} - Etat {self.etat}>"





