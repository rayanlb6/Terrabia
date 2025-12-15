from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Commande, Livraison
from .serializers import CommandeSerializer, LivraisonSerializer

# --- 1. Commande ViewSet ---
class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return Commande.objects.all().order_by('-created_at')
        return Commande.objects.filter(acheteur=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(acheteur=self.request.user)
    
    # GET /api/orders/historique/
    @action(detail=False, methods=['get'], url_path='historique')
    def historique(self, request):
        """Historique des commandes de l'utilisateur"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    # GET /api/orders/ventes/
    @action(detail=False, methods=['get'], url_path='ventes')
    def ventes(self, request):
        """Historique des ventes pour les agriculteurs"""
        user = request.user
        if user.role != 'agriculteur':
            return Response(
                {"detail": "Seuls les agriculteurs peuvent voir leurs ventes"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Récupérer les commandes contenant les produits de cet agriculteur
        commandes = Commande.objects.filter(
            lignes__produit__agriculteur=user
        ).distinct().order_by('-created_at')
        
        serializer = self.get_serializer(commandes, many=True)
        return Response(serializer.data)

# --- 2. Delivery ViewSet ---
class DeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Gère les livraisons. ReadOnly pour le moment.
    Inclut l'action 'accept' pour l'utilisateur 'livraison'.
    """
    queryset = Livraison.objects.all().order_by('-date_creation')
    serializer_class = LivraisonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return Livraison.objects.all()
        
        # Les livreurs ne voient que les livraisons à prendre ou les leurs
        if user.role == 'livraison':
            return Livraison.objects.filter(
                models.Q(statut='en_attente') | models.Q(agence=user)
            ).order_by('-date_creation')
        
        # Les autres ne voient rien via ce ViewSet
        return Livraison.objects.none()
    
    # POST /api/deliveries/accept/
    @action(detail=False, methods=['post'], url_path='accept')
    def accept(self, request):
        """
        Permet à l'agence de livraison d'accepter une livraison.
        """
        livraison_id = request.data.get('livraison_id')
        
        if not livraison_id:
            return Response(
                {"detail": "livraison_id requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        if user.role != 'livraison':
            return Response(
                {"detail": "Seul un agent de livraison peut accepter une livraison."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            livraison = Livraison.objects.get(id=livraison_id)
        except Livraison.DoesNotExist:
            return Response(
                {"detail": "Livraison introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if livraison.statut != 'en_attente':
            return Response(
                {"detail": f"La livraison est déjà {livraison.statut}."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mise à jour
        livraison.agence = user
        livraison.statut = 'attribuee'
        livraison.save()
        
        # Mettre à jour la commande associée
        commande = livraison.commande
        commande.statut = 'en_livraison'
        commande.save()
        
        serializer = LivraisonSerializer(livraison)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # POST /api/deliveries/validate/
    @action(detail=False, methods=['post'], url_path='validate')
    def validate(self, request):
        """
        Permet de marquer une livraison comme livrée.
        """
        livraison_id = request.data.get('livraison_id')
        notes = request.data.get('notes', '')
        
        if not livraison_id:
            return Response(
                {"detail": "livraison_id requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        
        try:
            livraison = Livraison.objects.get(id=livraison_id)
        except Livraison.DoesNotExist:
            return Response(
                {"detail": "Livraison introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier que c'est l'agence assignée ou un admin
        if user.role not in ['admin', 'livraison'] or (
            user.role == 'livraison' and livraison.agence != user
        ):
            return Response(
                {"detail": "Non autorisé"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mettre à jour
        livraison.statut = 'livree'
        livraison.save()
        
        # Mettre à jour la commande
        commande = livraison.commande
        commande.statut = 'livree'
        commande.save()
        
        serializer = LivraisonSerializer(livraison)
        return Response(serializer.data, status=status.HTTP_200_OK)