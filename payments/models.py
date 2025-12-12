from django.db import models
from orders.models import Commande # Assurez-vous d'importer la Commande

class Transaction(models.Model):
    commande = models.ForeignKey(
        Commande, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='transactions'
    )
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    # Référence interne de la transaction
    reference_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    # ID externe fourni par le processeur de paiement (Stripe/PayPal)
    processor_id = models.CharField(max_length=100, null=True, blank=True) 
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('succes', 'Succès'),
        ('echec', 'Échec'),
        ('rembourse', 'Remboursé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction #{self.id} - Montant: {self.montant} - Statut: {self.statut}"