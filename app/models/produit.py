from app import db
import json
from .associations import ProduitProjet

class Produit(db.Model):
    __tablename__ = 'produit'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=True)
    description = db.Column(db.String(255))
    materiaux = db.Column(db.String(100))
    categorie = db.Column(db.String(100))
    quantite = db.Column(db.Integer, default=0)


    # Association avec Projet (via la table intermédiaire ProduitProjet)
    projets_associes = db.relationship("ProduitProjet", back_populates="produit", cascade="all, delete-orphan")
    
    # Association avec Achat via LigneAchat
    lignes_achat = db.relationship("LigneAchat", back_populates="produit", cascade="all, delete-orphan")
    
    # Suivi des stocks
    stocks = db.relationship("Stock", back_populates="produit", cascade="all, delete-orphan")

    # Association avec CommandeProduction via LigneCommandeProduction (pas encore implenté)
    lignes_commande = db.relationship("LigneCommandeProduction", back_populates="produit", cascade="all, delete-orphan")


    def __init__(self, code=None, **kwargs):
        self.code = code
        for key, value in kwargs.items():
            setattr(self, key, value)


    def __repr__(self):
        return f"<Produit {self.code or 'sans code'}>"


    def crer_produit(self):
        """
        Creer le produit dans la base de données, si le code est unique.
        Lève une ValueError si le code existe déjà.
        """
        if self.code:
            existant = Produit.query.filter_by(code=self.code).first()
            if existant:
                raise ValueError(f"Produit {self.code} déjà existant.")

        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de l'enregistrement du produit : {e}")






    def modifier_produit(self, **kwargs):
        """Modifie les attributs du produit et sauvegarde les changements."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Produit {self.code} mis à jour avec succès.")



    @classmethod
    def recuperer_produit(cls, code):
        """Retourne le produit correspondant au code donné, ou None si non trouvé."""
        return cls.query.filter_by(code=code).first()

    def supprimer_produit(self):
        """Supprime ce produit de la base de données."""
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Produit {self.code} supprimé avec succès.")

    def associer_a_projet(self, projet, quantite):
        """
        Associe ce produit à un projet avec une quantité spécifique.
        Si le projet est invalide, la méthode affiche un message d'avertissement.
        """
        if not projet:
            print("⚠️ Projet invalide.")
            return
        lien = ProduitProjet(produit_id=self.id, projet_id=projet.id, quantite=quantite)
        db.session.add(lien)
        db.session.commit()
        print(f"✅ Produit {self.code} ajouté au projet {projet.code} avec quantité {quantite}.")

