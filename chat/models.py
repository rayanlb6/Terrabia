from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Message(models.Model):
    # L'expéditeur du message
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    # Le destinataire du message
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    
    # Le contenu du message
    content = models.TextField()
    
    # Horodatage
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Afficher les messages dans l'ordre chronologique (du plus récent au plus ancien)
        ordering = ['timestamp']

    def __str__(self):
        return f"De {self.sender.username} à {self.receiver.username} ({self.timestamp.strftime('%H:%M')})"