
class Produit:
    
    def __init__(self,description, code, type, emplacement=None, dimension=None, quantite=0, po=None):
        self.description = description
        self.code = code
        self.type = type
        self.po = po
        self.emplacement = emplacement
        self.dimension = dimension
        self.quantite = quantite
    
    def __str__(self):
        return f"Produit : {self.description} - Numéro : {self.code} - Type : {self.type} - Positionnement : {self.po} - Emplacement : {self.emplacement} - Dimension : {self.dimension} - Quantité : {self.quantite}"
    

