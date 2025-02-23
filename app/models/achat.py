import pandas as pd

class Achat():
    
    def __init__(self, projet=None, fichier=None):
        self.projet = projet
        self.fichier = fichier
        self.produits = []

    def importer_fichier(self, chemin_fichier):
        pass

    def definir_projet(self, projet):
        self.projet = projet

    #Sert pour les tests (pour l'instant)
    def ajouter_produit(self, produits):
        self.produits.extend(produits)