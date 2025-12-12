from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('agriculteur', 'Agriculteur'),
        ('acheteur', 'Acheteur'),
        ('livraison', 'Livraison'),
        ('admin', 'Admin')
    ]
    role = models.CharField(max_length=20, choices=ROLES)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
