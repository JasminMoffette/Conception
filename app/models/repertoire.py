
class Repertoire():
    def __init__(self):
        self.inventaires = []

    def ajouter_inventaire(self, inventaire):
        self.inventaires.append(inventaire)

    def __str__(self):
        return "\n".join(str(inventaire) for inventaire in self.inventaires)
    
    def recherche_produit(self, code):
        for inventaire in self.inventaires:
            for produit in inventaire.produits:
                if produit.code == code:
                    return produit
        return None
    
    