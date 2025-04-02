from app import db

class Emplacement(db.Model):
    __tablename__ = 'emplacement'
    
    id = db.Column(db.Integer, primary_key=True)
    entrepot = db.Column(db.String(100), nullable=False)
    cellule = db.Column(db.String(100), nullable=False)

    # Realation
    stocks = db.relationship("Stock", back_populates="emplacement", cascade="all, delete-orphan")


    def __init__(self, entrepot, cellule, **kwargs):
        self.entrepot = entrepot
        self.cellule = cellule
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<Emplacement {self.entrepot} - {self.cellule}>"


