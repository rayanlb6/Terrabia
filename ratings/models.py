from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Notation(models.Model):
    # L'utilisateur qui donne la note (doit être un acheteur)
    acheteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_donnees')
    
    # L'utilisateur qui reçoit la note (doit être un agriculteur)
    agriculteur = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notes_recues',
        limit_choices_to={'role': 'agriculteur'} # S'assurer que seul un agriculteur reçoit la note
    )
    
    # Note (de 1 à 5, par exemple)
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Commentaire optionnel
    commentaire = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Assurer qu'un acheteur ne peut noter un agriculteur qu'une fois par... (par exemple, par commande ou par mois)
        # Pour simplifier, nous n'ajoutons pas de contrainte ici.
        pass

    def __str__(self):
        return f"Note de {self.note} par {self.acheteur.username} à {self.agriculteur.username}"