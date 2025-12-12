from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('statut', 'created_at', 'reference_id', 'processor_id')

# Serializer pour la validation des données entrantes de paiement
class PaymentSerializer(serializers.Serializer):
    commande_id = serializers.IntegerField()
    payment_token = serializers.CharField(max_length=255) # Token de carte généré côté client
    # Vous pouvez ajouter ici d'autres détails nécessaires au paiement