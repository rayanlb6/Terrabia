from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Produit, Panier
from .serializers import ProduitSerializer, PanierSerializer

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # Ajoutez JSONParser
    
    def perform_create(self, serializer):
        serializer.save(agriculteur=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='mes-produits')
    def mes_produits(self, request):
        produits = Produit.objects.filter(agriculteur=request.user)
        serializer = self.get_serializer(produits, many=True)
        return Response(serializer.data)


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Panier
from .serializers import PanierSerializer
from products.models import Produit

class PanierViewSet(viewsets.ModelViewSet):
    serializer_class = PanierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Panier.objects.filter(acheteur=self.request.user)

    def create(self, request, *args, **kwargs):
        produit_id = request.data.get("produit_id")
        quantite = int(request.data.get("quantite", 1))

        if not produit_id:
            return Response(
                {"detail": "produit_id requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        produit = get_object_or_404(Produit, id=produit_id)

        panier_item, created = Panier.objects.get_or_create(
            acheteur=request.user,
            produit=produit,
            defaults={"quantite": quantite}
        )

        if not created:
            panier_item.quantite += quantite
            panier_item.save()

        serializer = self.get_serializer(panier_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
