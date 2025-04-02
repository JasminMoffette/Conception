from app import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    poste = db.Column(db.String(50), nullable=False)


    def __init__(self, nom, mot_de_passe, poste):
        self.nom = nom
        self.set_password(mot_de_passe)
        self.poste = poste
    
    def __repr__(self):
        return f"<Utilisateur {self.nom} ({self.poste})>"