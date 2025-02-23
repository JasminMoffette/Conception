class Produit:
    def __init__(self, code, description=None, materiaux=None, categorie=None, po=None, emplacement=None, dimension=None, projet=None, quantite=0, cp=None, fournisseur=None, coupe=None, no_catalogue=None, fsc=None, historique=None):
        """
        Initialise un produit de l'inventaire.
        :param code: Numéro d'identification du produit en lien avec les dessins
        :param description: Description du produit
        :param materiaux: Type de matériel
        :param categorie: Catégorie du produit
        :param po: Numéro de commande d'achat associé à ce produit
        :param emplacement: Emplacement du produit (usine, entrepôt, cellule)
        :param dimension: Dimensions du produit (épaisseur, largeur, longueur)
        :param projet: Projet lié à ce produit
        :param quantite: Quantité de ce produit calculée avec le code (par défaut 0)
        :param cp: Commande de production liée à ce produit
        :param fournisseur: Fournisseur du produit
        :param coupe: Type de coupe du produit
        :param no_catalogue: Numéro du catalogue du produit Maestro
        :param fsc: FSC du produit
        :param historique: Historique des déplacements du produit (dates entre chaque module)
        """
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
        self.historique = historique if historique is not None else []
    
    def mettre_a_jour_quantite(self, quantite):
        """Met à jour la quantité en stock du produit."""
        self.quantite = quantite
        self.historique.append(f"Mise à jour quantité: {quantite}")
    
    def ajuster_quantite(self, quantite):
        """Ajuste la quantité du produit en ajoutant ou en retirant des unités."""
        self.quantite += quantite
        mouvement = f"Ajout de {quantite}" if quantite > 0 else f"Retrait de {-quantite}"
        self.historique.append(mouvement)
    
    def obtenir_valeur_stock(self, prix_unitaire):
        """Calcule la valeur totale du stock pour ce produit."""
        return self.quantite * prix_unitaire
    
    def afficher_historique(self):
        """Affiche l'historique des mouvements de stock."""
        return '\n'.join(self.historique) if self.historique else "Aucun mouvement enregistré"
    
    def __str__(self):
        return f"Produit({self.code}): {self.description if self.description else 'Non défini'}, Matériau: {self.materiaux if self.materiaux else 'Non défini'}, Catégorie: {self.categorie if self.categorie else 'Non défini'}, Stock: {self.quantite}, Fournisseur: {self.fournisseur if self.fournisseur else 'Non défini'}, Projet: {self.projet if self.projet else 'Non assigné'}, Emplacement: {self.emplacement if self.emplacement else 'Non défini'}"


# Exemple d'utilisation
if __name__ == "__main__":
    produit1 = Produit("BOIS123", "Panneau MDF", "Bois", "Panneaux", "PO987", "Entrepôt A1", (20, 100, 200), "PROJ001", 50, "CP123", "Fournisseur A", "Sciage", "CAT456", "FSC123")
    print(produit1)
    produit1.ajuster_quantite(-10)
    print(f"Nouvelle quantité : {produit1.quantite}")
    print("Historique des mouvements:")
    print(produit1.afficher_historique())




