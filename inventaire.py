import repertoire
import produit

class Inventaire():

    def __init__(self, numero):
        super().__init__()
        self.produits = []
        self.numero = numero

    def ajouter_produit(self, ajout=produit.Produit):
            for produit in self.produits:
                if produit.code == ajout.code:
                    produit.quantite += ajout.quantite
                else:
                    self.produits.append(ajout)
            
    def __str__(self):
        return f"Projet n°{self.numero}:\n" + "\n".join(str(produit) for produit in self.produits)
    