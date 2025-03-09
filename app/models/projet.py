from app import db
from datetime import datetime
from .produit_projet import ProduitProjet



class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  # Identifiant unique
    nom = db.Column(db.String(100), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)  # Date automatique
    responsable = db.Column(db.String(100))
    statut = db.Column(db.String(50))

    # Relation many-to-many avec Produit via ProduitProjet
    produits_associes = db.relationship("ProduitProjet", back_populates="projet", cascade="all, delete-orphan")

    def __init__(self, code, nom, responsable=None, statut=None, date_creation=None):
        self.code = code
        self.nom = nom
        self.responsable = responsable
        self.statut = statut
        self.date_creation = date_creation or datetime.utcnow()

    def __repr__(self):
        return f"<Projet {self.code} - {self.nom}>"

    @classmethod
    def ajouter_projet(cls, code, nom, responsable=None, statut=None):
        projet_existant = cls.query.filter_by(code=code).first()
        if projet_existant:
            print(f"⚠️ Projet '{code}' existe déjà.")
            return projet_existant

        nouveau_projet = cls(code=code, nom=nom, responsable=responsable, statut=statut)
        db.session.add(nouveau_projet)
        db.session.commit()
        print(f"✅ Projet '{code}' ajouté avec succès.")
        return nouveau_projet

    @classmethod
    def recuperer_projet(cls, code):
        return cls.query.filter_by(code=code).first()

    def modifier_projet(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Projet {self.code} mis à jour avec succès.")

    def supprimer_projet(self):
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Projet {self.code} supprimé avec succès.")

    def ajouter_produit(self, produit, quantite):
        """Associe un produit à ce projet avec une quantité spécifique."""
        if not produit:
            print("⚠️ Produit invalide.")
            return

        lien = ProduitProjet(produit_id=produit.id, projet_id=self.id, quantite=quantite)
        db.session.add(lien)
        db.session.commit()
        print(f"✅ Produit {produit.code} ajouté au projet {self.code} avec quantité {quantite}.")
