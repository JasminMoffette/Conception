from app import db
from datetime import datetime

class Reception(db.Model):
    __tablename__ = 'reception'
    
    id = db.Column(db.Integer, primary_key=True)
    date_reception = db.Column(db.DateTime, default=datetime.utcnow)
    achat_id = db.Column(db.Integer, db.ForeignKey('achat.id'), nullable=False)
    etat = db.Column(db.String(20), default=None)

    # Relation pour accéder aux lignes de réception associées
    lignes_reception = db.relationship("LigneReception", back_populates="reception", cascade="all, delete-orphan")

    def __init__(self, achat_id, **kwargs):
        self.achat_id = achat_id
        self.date_reception = kwargs.get("date_reception", datetime.utcnow())
        self.etat = kwargs.get("etat", None)

    def __repr__(self):
        return f"<Reception Achat {self.achat_id} - ID {self.id} - Etat {self.etat}>"

    def ajouter_reception(self):
        db.session.add(self)
        db.session.commit()
        print(f"✅ Réception pour Achat {self.achat_id} ajoutée avec succès.")

    def modifier_reception(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        print(f"✅ Réception {self.id} mise à jour avec succès.")

    def supprimer_reception(self):
        db.session.delete(self)
        db.session.commit()
        print(f"🗑️ Réception {self.id} supprimée avec succès.")

    def confirmer_reception(self, emplacements_produits):
        """
        Confirme la réception en mettant à jour :
        - le stock global de chaque produit
        - la quantité reçue dans ProduitProjet
        - l'attribution des emplacements via la classe Stock

        emplacements_produits: dict {produit_id: emplacement_id}
        """
        achat_instance = self.achat
        if not achat_instance:
            print("⚠️ Achat associé introuvable.")
            return

        projet_id = achat_instance.projet_id
        reception_complete = True

        for ligne in self.lignes_reception:
            produit = ligne.produit
            if produit:
                produit.quantite += ligne.quantite_recue

                # Mise à jour ProduitProjet (comme actuellement)
                if projet_id:
                    from app.models.associations import ProduitProjet
                    association = ProduitProjet.query.filter_by(produit_id=produit.id, projet_id=projet_id).first()
                    if association:
                        if hasattr(association, 'quantite_recue'):
                            association.quantite_recue += ligne.quantite_recue
                        else:
                            association.quantite_recue = ligne.quantite_recue

                # Nouvelle étape : enregistrer dans Stock avec emplacement choisi
                emplacement_id = emplacements_produits.get(produit.id)
                if emplacement_id:
                    from app.models.associations import Stock
                    stock = Stock(
                        produit_id=produit.id,
                        emplacement_id=emplacement_id,
                        quantite=ligne.quantite_recue,
                        achat_id=self.achat_id  # ici, l'achat_id est très utile
                    )
                    db.session.add(stock)
                else:
                    print(f"⚠️ Aucun emplacement attribué pour produit {produit.code}.")
                    reception_complete = False
            else:
                print(f"⚠️ Produit avec id {ligne.produit_id} non trouvé.")
                reception_complete = False

        self.etat = "complete" if reception_complete else "partielle"
        db.session.commit()
        print(f"✅ Réception {self.id} confirmée : stocks et associations mis à jour. État: {self.etat}")


        # Déterminer l'état de la réception
        self.etat = "complete" if reception_complete else "partielle"
        db.session.commit()
        print(f"✅ Réception {self.id} confirmée : stocks et associations mis à jour. Etat: {self.etat}")

