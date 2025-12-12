from rest_framework import viewsets, permissions
from .models import Produit, Panier
from .serializers import ProduitSerializer, PanierSerializer

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

    def perform_create(self, serializer):
        serializer.save(agriculteur=self.request.user)

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class PanierViewSet(viewsets.ModelViewSet):
    queryset = Panier.objects.all()
    serializer_class = PanierSerializer

    def get_queryset(self):
        user = self.request.user
        return Panier.objects.filter(acheteur=user)

    def perform_create(self, serializer):
        serializer.save(acheteur=self.request.user)
