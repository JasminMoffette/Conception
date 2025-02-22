
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
        return f"Produit : {self.description} - Numéro : {self.code} - Type : {self.type} - production order : {self.po} - Emplacement : {self.emplacement} - Dimension : {self.dimension} - Quantité : {self.quantite}"
    
    def ajouter_quantite(self, quantite):
        self.quantite += quantite
    
    def retirer_quantite(self, quantite):
        self.quantite -= quantite
    
    def definir_emplacement(self, emplacement):
        self.emplacement = emplacement
    
    def definir_dimension(self, dimension):
        self.dimension = dimension
    
    def definir_po(self, po):
        self.po = po
    


