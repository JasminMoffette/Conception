import achat
import ajustement
import inventaire
import production
import produit
import reception
import repertoire

achat_test = achat.Achat(projet="001")
produits_test = [produit.Produit("Ordinateur portable", "OP001", "Électronique", po="PO12345", quantite=5),
    produit.Produit("Souris sans fil", "SS001", "Accessoire", po="PO12345", emplacement="Étagère A", quantite=20),
    produit.Produit("Écran 24 pouces", "EC001", "Électronique", po="PO12346", dimension="24x18x2", quantite=10),
    produit.Produit("Clavier mécanique", "CM001", "Accessoire", po="PO12347", emplacement="Étagère B", dimension="18x6x1", quantite=15),
    produit.Produit("Câble HDMI", "CH001", "Accessoire", po="PO12348", quantite=50)]


inventaire_test = inventaire.Inventaire("001")
for i in produits_test:
    inventaire_test.ajouter_produit(i)

print(inventaire_test.produits)
repertoire_test = repertoire.Repertoire()
repertoire_test.ajouter_inventaire(inventaire_test)

print(produits_test[0])
print(produits_test)
print(repertoire_test.inventaires)
print(inventaire_test)