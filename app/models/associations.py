from app import db

# Association entre Produit et Projet (many-to-many)
class ProduitProjet(db.Model):
    __tablename__ = 'produitprojet'
    id = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    projet_id = db.Column(db.Integer, db.ForeignKey('projet.id'), nullable=False)
    quantite = db.Column(db.Integer, default=0)

    # Relations bidirectionnelles
    produit = db.relationship("Produit", back_populates="projets_associes")
    projet = db.relationship("Projet", back_populates="produits_associes")

    def __init__(self, produit_id, projet_id, quantite):
        self.produit_id = produit_id
        self.projet_id = projet_id
        self.quantite = quantite

    def __repr__(self):
        return f"<ProduitProjet produit_id={self.produit_id}, projet_id={self.projet_id}, quantite={self.quantite}>"


# Association entre Achat et Produit pour détailler un Achat
class LigneAchat(db.Model):
    __tablename__ = 'ligneachat'
    id = db.Column(db.Integer, primary_key=True)
    quantite = db.Column(db.Integer, default=0)
    achat_id = db.Column(db.Integer, db.ForeignKey('achat.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)

    # Relations bidirectionnelles
    achat = db.relationship("Achat", back_populates="lignes_achat")
    produit = db.relationship("Produit", back_populates="lignes_achat")

    def __init__(self, achat_id, produit_id, quantite):
        self.achat_id = achat_id
        self.produit_id = produit_id
        self.quantite = quantite

    def __repr__(self):
        return f"<LigneAchat achat_id={self.achat_id}, produit_id={self.produit_id}, quantite={self.quantite}>"
    

# Association entre CommandeProduction et Produit pour détailler une commande de production
class LigneCommandeProduction(db.Model):
    __tablename__ = 'lignecommandeproduction'
    id = db.Column(db.Integer, primary_key=True)
    quantite = db.Column(db.Integer, default=0)
    commande_production_id = db.Column(db.Integer, db.ForeignKey('commandeproduction.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)

    # Relations bidirectionnelles
    commande_production = db.relationship("CommandeProduction", back_populates="lignes_commande")
    produit = db.relationship("Produit", back_populates="lignes_commande")

    def __init__(self, commande_production_id, produit_id, quantite):
        self.commande_production_id = commande_production_id
        self.produit_id = produit_id
        self.quantite = quantite

    def __repr__(self):
        return f"<LigneCommandeProduction commande_production_id={self.commande_production_id}, produit_id={self.produit_id}, quantite={self.quantite}>"
    
# relation entre achat et reception
class LigneReception(db.Model):
    __tablename__ = 'lignereception'
    id = db.Column(db.Integer, primary_key=True)
    quantite_recue = db.Column(db.Integer, default=0)
    reception_id = db.Column(db.Integer, db.ForeignKey('reception.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)

    # Relations bidirectionnelles
    reception = db.relationship("Reception", back_populates="lignes_reception")
    produit = db.relationship("Produit", backref="lignes_reception_detail")

    def __init__(self, reception_id, produit_id, quantite_recue):
        self.reception_id = reception_id
        self.produit_id = produit_id
        self.quantite_recue = quantite_recue

    def __repr__(self):
        return f"<LigneReception reception_id={self.reception_id}, produit_id={self.produit_id}, quantite_recue={self.quantite_recue}>"
   


# Association entre Produit et Emplacement pour le suivi des stocks
class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    quantite = db.Column(db.Integer, default=0)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    emplacement_id = db.Column(db.Integer, db.ForeignKey('emplacement.id'), nullable=False)

    # Relations bidirectionnelles
    produit = db.relationship("Produit", back_populates="stocks")
    emplacement = db.relationship("Emplacement", back_populates="stocks")

    def __init__(self, produit_id, emplacement_id, quantite):
        self.produit_id = produit_id
        self.emplacement_id = emplacement_id
        self.quantite = quantite

    def __repr__(self):
        return f"<Stock produit_id={self.produit_id}, emplacement_id={self.emplacement_id}, quantite={self.quantite}>"

