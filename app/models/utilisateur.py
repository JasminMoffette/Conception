from app import db

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    poste = db.Column(db.String(50), nullable=False)