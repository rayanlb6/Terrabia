from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action # Importation CRUCIALE pour les actions personnalisées
from rest_framework.response import Response
from .models import Commande, Livraison
from .serializers import CommandeSerializer, LivraisonSerializer # Nécessite LivraisonSerializer

# --- 1. Commande ViewSet ---
class CommandeViewSet(viewsets.ModelViewSet):
    # ... (Le code existant pour queryset, serializer_class, permission_classes)
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # acheteur sees own orders, staff/admin can see all (Ceci couvre déjà l'historique de base)
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return Commande.objects.all().order_by('-created_at')
        return Commande.objects.filter(acheteur=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(acheteur=self.request.user)
    
    # GET /api/orders/history/
    @action(detail=False, methods=['get'])
    def history(self, request):
        """ Alias pour l'historique des commandes de l'utilisateur """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# --- 2. Delivery ViewSet (pour /deliveries/accept/) ---
class DeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Gère les livraisons. ReadOnly pour le moment.
    Inclut l'action 'accept' pour l'utilisateur 'livraison'.
    """
    # L'agence de livraison doit voir seulement les livraisons 'en_attente' ou celles qui lui sont 'attribuees'
    queryset = Livraison.objects.all().order_by('-date_creation')
    serializer_class = LivraisonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return Livraison.objects.all()
        
        # Les livreurs ne voient que les livraisons à prendre ou les leurs.
        if user.role == 'livraison':
            return Livraison.objects.filter(
                models.Q(statut='en_attente') | models.Q(agence=user)
            ).order_by('-date_creation')
        
        # Les autres ne voient rien via ce ViewSet
        return Livraison.objects.none()

    # POST /api/deliveries/{pk}/accept/
    @action(detail=True, methods=['post'], url_path='accept', permission_classes=[permissions.IsAuthenticated])
    def accept_delivery(self, request, pk=None):
        """
        Permet à l'agence de livraison d'accepter une livraison et de la marquer comme 'attribuee'.
        """
        livraison = self.get_object() 
        user = request.user
        
        if user.role != 'livraison':
            return Response({"detail": "Seul un agent de livraison peut accepter une livraison."}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        if livraison.statut != 'en_attente':
            return Response({"detail": f"La livraison est déjà {livraison.statut}."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Mise à jour
        livraison.agence = user
        livraison.statut = 'attribuee'
        livraison.save()

        # Mettre à jour la commande associée
        commande = livraison.commande
        commande.statut = 'attribuee'
        commande.save()

        return Response(LivraisonSerializer(livraison).data, status=status.HTTP_200_OK)