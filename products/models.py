from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Produit(models.Model):
    agriculteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produits')
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Panier(models.Model):
    acheteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='panier')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    class Meta:
        unique_together = ("acheteur", "produit")
