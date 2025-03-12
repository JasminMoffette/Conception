from app import db
from datetime import datetime

class Projet(db.Model):
    __tablename__ = 'projet'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  
    nom = db.Column(db.String(100), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    responsable = db.Column(db.String(100))
    statut = db.Column(db.String(50))

    # Relations avec Achat et CommandeProduction
    achats = db.relationship("Achat", backref="projet", cascade="all, delete-orphan")
    commandes_production = db.relationship("CommandeProduction", backref="projet", cascade="all, delete-orphan")
    
    # Relation many-to-many avec Produit via la table intermédiaire ProduitProjet
    produits_associes = db.relationship("ProduitProjet", back_populates="projet", cascade="all, delete-orphan")

    def __init__(self, code, **kwargs):
        self.code = code
        self.nom = kwargs.get("nom")
        self.responsable = kwargs.get("responsable")
        self.statut = kwargs.get("statut")
        self.date_creation = kwargs.get("date_creation", datetime.utcnow())

    def __repr__(self):
        return f"<Projet {self.code} - {self.nom}>"

    def ajouter_projet(self):
        """Ajoute ce projet dans la base de données."""
        db.session.add(self)
        db.session.commit()
        print(f"✅ Projet {self.code} ajouté avec succès.")

    def modifier_projet(self, **kwargs):
        """Modifie les attributs de ce projet et sauvegarde les changements."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Projet {self.code} mis à jour avec succès.")

    @classmethod
    def recuperer_projet(cls, code):
        """Retourne le projet correspondant au code donné, ou None s'il n'existe pas."""
        return cls.query.filter_by(code=code).first()

    def supprimer_projet(self):
        """Supprime ce projet de la base de données."""
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Projet {self.code} supprimé avec succès.")

    def associer_achat(self, achat):
        """
        Associe un achat à ce projet en mettant à jour la clé étrangère de l'achat.
        """
        if not achat:
            print("⚠️ Achat invalide.")
            return
        achat.projet_id = self.id
        db.session.add(achat)
        db.session.commit()
        print(f"✅ Achat {achat.po} associé au projet {self.code}.")

    def associer_commandeProduction(self, commande):
        """
        Associe une commande de production à ce projet en mettant à jour la clé étrangère de la commande.
        """
        if not commande:
            print("⚠️ CommandeProduction invalide.")
            return
        commande.projet_id = self.id
        db.session.add(commande)
        db.session.commit()
        print(f"✅ CommandeProduction {commande.cp} associée au projet {self.code}.")
