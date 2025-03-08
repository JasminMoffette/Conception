from app import db
from datetime import datetime

class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  # attribut principal pour identifier clairement
    nom = db.Column(db.String(100), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)  # date automatique à la création
    responsable = db.Column(db.String(100))
    statut = db.Column(db.String(50))

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

        nouveau_projet = cls(
            code=code,
            nom=nom,
            responsable=responsable,
            statut=statut
        )
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
