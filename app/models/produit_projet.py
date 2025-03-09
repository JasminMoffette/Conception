from app import db

class ProduitProjet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id'), nullable=False)
    quantite = db.Column(db.Integer, default=1, nullable=False)  

    # Relations avec Produit et Projet
    produit = db.relationship("Produit", back_populates="projets_associes")
    projet = db.relationship("Projet", back_populates="produits_associes")

    def __init__(self, produit_id, projet_id, quantite=1):
        self.produit_id = produit_id
        self.projet_id = projet_id
        self.quantite = quantite

    def __repr__(self):
        return f"<ProduitProjet produit_id={self.produit_id} projet_id={self.projet_id} quantite={self.quantite}>"
