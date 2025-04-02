from app import db
from datetime import date

class Projet(db.Model):
    __tablename__ = 'projet'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  
    nom = db.Column(db.String(100))
    date_creation = db.Column(db.Date, default=date.today)
    responsable = db.Column(db.String(100))
    statut = db.Column(db.String(50))

    # Relations 
    achats = db.relationship("Achat", backref="projet", cascade="all, delete-orphan")
    commandes_production = db.relationship("CommandeProduction", backref="projet", cascade="all, delete-orphan")
    produits_associes = db.relationship("ProduitProjet", back_populates="projet", cascade="all, delete-orphan")

    def __init__(self, code, **kwargs):
        self.code = code
        self.nom = kwargs.get("nom")
        self.responsable = kwargs.get("responsable")
        self.statut = kwargs.get("statut")
        self.date_creation = kwargs.get("date_creation", date.today())

    def __repr__(self):
        return f"<Projet {self.code} - {self.nom}>"




 
