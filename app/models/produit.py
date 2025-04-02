from app import db

class Produit(db.Model):
    __tablename__ = 'produit'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=True)
    description = db.Column(db.String(255))
    materiaux = db.Column(db.String(100))
    categorie = db.Column(db.String(100))
    quantite = db.Column(db.Integer, default=0)


    # Association 
    projets_associes = db.relationship("ProduitProjet", back_populates="produit", cascade="all, delete-orphan")
    lignes_achat = db.relationship("LigneAchat", back_populates="produit", cascade="all, delete-orphan")
    stocks = db.relationship("Stock", back_populates="produit", cascade="all, delete-orphan")
    lignes_commande = db.relationship("LigneCommandeProduction", back_populates="produit", cascade="all, delete-orphan")


    def __init__(self, code=None, **kwargs):
        self.code = code
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<Produit {self.code or 'sans code'}>"

    def creer_produit(self):
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
        
    

    @classmethod
    def creer_depuis_formulaire(cls, form):
        code = form.get("code") or None
        data = {}
        for key in ["description", "materiaux", "categorie", "quantite"]:
            value = form.get(key)
            if value:
                if key == "quantite":
                    try:
                        value = int(value)
                    except ValueError:
                        raise ValueError("La quantité doit être un nombre entier.")
                data[key] = value

        # Création du produit
        produit = cls(code=code, **data)
        produit.creer_produit()
        return produit
















   