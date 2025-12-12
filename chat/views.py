from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
    Gère la création (POST) et la consultation de l'historique des messages (GET /api/messages/).
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Un utilisateur ne voit que les messages qu'il a envoyés OU reçus
        return self.queryset.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        ).select_related('sender', 'receiver').order_by('timestamp')

    # Redéfinir la méthode POST pour définir automatiquement l'expéditeur
    def perform_create(self, serializer):
        # L'expéditeur est toujours l'utilisateur actuellement authentifié
        serializer.save(sender=self.request.user)
        
    # GET /api/messages/ peut être filtré par ?receiver_id=X pour voir une conversation spécifique
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Filtre pour une conversation spécifique (optionnel)
        receiver_id = request.query_params.get('receiver_id')
        if receiver_id:
            queryset = queryset.filter(
                models.Q(sender_id=receiver_id) | models.Q(receiver_id=receiver_id)
            )
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)