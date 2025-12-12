from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Commande(models.Model):
    acheteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.acheteur}"

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey('products.Produit', on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

class Livraison(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='livraison')
    agence = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='livraisons')
    statut = models.CharField(max_length=20, default='en_attente')
    updated_at = models.DateTimeField(auto_now=True)
