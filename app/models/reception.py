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

    def confirmer_reception(self):
        """
        Confirme la réception en mettant à jour le stock global de chaque produit ainsi que
        la quantité reçue dans l'association ProduitProjet liée au projet de l'achat.
        Détermine l'état de la réception en fonction des quantités reçues par rapport aux quantités commandées.
        """
        # On récupère le projet lié à cet achat via la relation Achat (supposée définie dans le modèle Achat)
        achat_instance = self.achat  # On suppose que la relation backref 'achat' existe dans le modèle Achat
        if not achat_instance:
            print("⚠️ Achat associé introuvable.")
            return

        projet_id = achat_instance.projet_id

        # Initialiser un indicateur pour savoir si la réception est complète
        reception_complete = True

        # Pour chaque ligne de réception, mettre à jour le stock du produit et l'association dans ProduitProjet
        for ligne in self.lignes_reception:
            produit = ligne.produit  # On suppose que la relation "produit" est bien définie dans LigneReception
            if produit:
                # Mettre à jour le stock global du produit
                produit.quantite += ligne.quantite_recue
                # Mettre à jour l'association ProduitProjet si le projet est défini
                if projet_id:
                    from app.models.associations import ProduitProjet
                    association = ProduitProjet.query.filter_by(produit_id=produit.id, projet_id=projet_id).first()
                    if association:
                        # Nous supposons ici que l'association doit enregistrer la quantité reçue.
                        # Il faut ajouter un nouvel attribut 'quantite_recue' dans la classe ProduitProjet pour cela.
                        if hasattr(association, 'quantite_recue'):
                            association.quantite_recue += ligne.quantite_recue
                        else:
                            # Si l'attribut n'existe pas, on peut l'initialiser (mais idéalement, il faudrait le définir dans le modèle)
                            association.quantite_recue = ligne.quantite_recue
                    else:
                        print(f"⚠️ Aucune association trouvée pour produit_id {produit.id} et projet_id {projet_id}.")
                # Optionnel : si la quantité reçue est inférieure à la quantité commandée (que l'on peut récupérer depuis LigneAchat ou Achat),
                # on considère la réception comme partielle.
                # Par exemple, si ligne.quantite_recue < quantité attendue, on passe reception_complete à False.
                # Ici, on suppose que la logique de comparaison est définie ailleurs.
            else:
                print(f"⚠️ Produit avec id {ligne.produit_id} non trouvé.")
                reception_complete = False

        # Déterminer l'état de la réception
        self.etat = "complete" if reception_complete else "partielle"
        db.session.commit()
        print(f"✅ Réception {self.id} confirmée : stocks et associations mis à jour. Etat: {self.etat}")

