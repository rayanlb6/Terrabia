from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Commande(models.Model):
    acheteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=20, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # AJOUTEZ CES DEUX CHAMPS
    adresse_livraison = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    
    def __str__(self):
        return f"Commande #{self.id} - {self.acheteur}"

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey('products.Produit', on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantite}x {self.produit.nom}"

class Livraison(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, related_name='livraison')
    agence = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'livraison'},
        related_name='livraisons_gerees'
    )
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('attribuee', 'Attribuée'),
        ('en_transit', 'En transit'),
        ('livree', 'Livrée'),
        ('echec', 'Échec de livraison'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Livraison pour Commande #{self.commande.id} - Statut: {self.statut}"