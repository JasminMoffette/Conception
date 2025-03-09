from app import db
import json
from .produit_projet import ProduitProjet




class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    materiaux = db.Column(db.String(100))
    categorie = db.Column(db.String(100))
    po = db.Column(db.String(50))
    statut = db.Column(db.String(50))
    emplacement = db.Column(db.String(100))
    dimension = db.Column(db.String(100))
    quantite = db.Column(db.Integer, default=0) 
    cp = db.Column(db.String(100))
    fournisseur = db.Column(db.String(100))
    coupe = db.Column(db.String(50))
    no_catalogue = db.Column(db.String(100))
    fsc = db.Column(db.String(50))
    historique = db.Column(db.Text)  # Stocké en JSON

    # Relation many-to-many avec Projet via ProduitProjet
    projets_associes = db.relationship("ProduitProjet", back_populates="produit", cascade="all, delete-orphan")

    def __init__(self, code, **kwargs):
        self.code = code
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.historique = json.dumps(kwargs.get('historique', []))

    def ajouter_produit(self):
        db.session.add(self)
        db.session.commit()
        print(f"✅ Produit {self.code} ajouté avec succès.")

    def modifier_produit(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Produit {self.code} mis à jour avec succès.")

    @classmethod
    def recuperer_produit(cls, code):
        return cls.query.filter_by(code=code).first()

    def supprimer_produit(self):
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Produit {self.code} supprimé avec succès.")

    def associer_a_projet(self, projet, quantite):
        """ Associe ce produit à un projet avec une quantité spécifique. """
        if not projet:
            print("⚠️ Projet invalide.")
            return

        lien = ProduitProjet(produit_id=self.id, projet_id=projet.id, quantite=quantite)
        db.session.add(lien)
        db.session.commit()
        print(f"✅ Produit {self.code} ajouté au projet {projet.code} avec quantité {quantite}.")

