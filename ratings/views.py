from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Notation
from .serializers import RatingSerializer

class RatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des notations.
    Permet aux utilisateurs authentifiés (acheteurs) de donner une note (POST).
    """
    queryset = Notation.objects.all().order_by('-created_at')
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Limiter l'accès aux notes créées par l'utilisateur courant (pour des raisons de sécurité)
    def get_queryset(self):
        # Les agriculteurs peuvent voir les notes qu'ils ont reçues.
        if self.request.user.role == 'agriculteur':
            return self.queryset.filter(agriculteur=self.request.user)
        # Les acheteurs peuvent voir les notes qu'ils ont données.
        return self.queryset.filter(acheteur=self.request.user)
    
    # Assurer que l'acheteur est automatiquement défini lors de la création
    def perform_create(self, serializer):
        user = self.request.user
        
        # Vérification si l'utilisateur est un acheteur (optionnel, mais bonne pratique)
        if user.role != 'acheteur':
             raise permissions.PermissionDenied("Seuls les acheteurs peuvent donner des notes.")
             
        # La ligne cruciale : enregistrer l'acheteur courant
        serializer.save(acheteur=user)