from rest_framework import viewsets, permissions
from .models import Commande, Livraison
from .serializers import CommandeSerializer

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # acheteur sees own orders, staff/admin can see all
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return Commande.objects.all()
        return Commande.objects.filter(acheteur=user)

    def perform_create(self, serializer):
        serializer.save(acheteur=self.request.user)
