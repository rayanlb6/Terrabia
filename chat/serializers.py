from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    # Afficher le nom d'utilisateur de l'expéditeur et du destinataire
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'sender_username', 'receiver', 'receiver_username', 'content', 'timestamp')
        read_only_fields = ('id', 'sender', 'sender_username', 'receiver_username', 'timestamp')
        # Note: 'receiver' n'est pas en read_only pour la création (POST)