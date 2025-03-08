from app import db
import json

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
    projet = db.Column(db.String(100))
    quantite = db.Column(db.Integer, default=0)
    cp = db.Column(db.String(100))
    fournisseur = db.Column(db.String(100))
    coupe = db.Column(db.String(50))
    no_catalogue = db.Column(db.String(100))
    fsc = db.Column(db.String(50))
    historique = db.Column(db.Text)  # Stocké en JSON

    def __init__(self, code, description=None, materiaux=None, categorie=None, po=None, emplacement=None, dimension=None, projet=None, quantite=0, cp=None, fournisseur=None, coupe=None, no_catalogue=None, fsc=None, historique=None):
        self.code = code
        self.description = description
        self.materiaux = materiaux
        self.categorie = categorie
        self.po = po
        self.emplacement = emplacement
        self.dimension = dimension
        self.projet = projet
        self.quantite = quantite
        self.cp = cp
        self.fournisseur = fournisseur
        self.coupe = coupe
        self.no_catalogue = no_catalogue
        self.fsc = fsc
        self.historique = json.dumps(historique) if historique else json.dumps([])

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
