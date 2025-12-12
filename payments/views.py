from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction

from orders.models import Commande
from .models import Transaction
from .serializers import PaymentSerializer, TransactionSerializer

class PaymentProcessorView(APIView):
    """
    Gère le traitement des paiements. 
    URL: POST /api/payments/process/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        commande_id = serializer.validated_data['commande_id']
        payment_token = serializer.validated_data['payment_token']
        
        try:
            commande = Commande.objects.get(id=commande_id, acheteur=request.user)
        except Commande.DoesNotExist:
            return Response({"detail": "Commande non trouvée ou vous n'êtes pas l'acheteur."}, 
                            status=status.HTTP_404_NOT_FOUND)

        if commande.statut != 'en_attente':
            return Response({"detail": f"La commande est déjà au statut '{commande.statut}' et ne peut pas être payée."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # --- LOGIQUE DE TRAITEMENT DE PAIEMENT SIMULÉE ---
        try:
            # Cette section est là où vous intégreriez la librairie externe (Stripe, etc.)
            # Simuler l'appel à l'API de paiement
            
            # Pour l'exemple, nous simulons un succès
            is_successful = (payment_token != 'token_echec') 
            
            if is_successful:
                # Créer la transaction et mettre à jour le statut de la commande de manière atomique
                with transaction.atomic():
                    # 1. Enregistrement de la transaction
                    transaction_obj = Transaction.objects.create(
                        commande=commande,
                        montant=commande.total,
                        reference_id=f"REF-{commande.id}-{Transaction.objects.count() + 1}",
                        processor_id="PROC_12345", # ID fourni par le service externe
                        statut='succes'
                    )
                    # 2. Mise à jour du statut de la Commande
                    commande.statut = 'payee'
                    commande.save()

                return Response({
                    "message": "Paiement traité avec succès.",
                    "transaction": TransactionSerializer(transaction_obj).data
                }, status=status.HTTP_200_OK)
            else:
                # Simuler un échec
                Transaction.objects.create(
                    commande=commande,
                    montant=commande.total,
                    statut='echec'
                )
                return Response({"detail": "Le paiement a échoué. Veuillez réessayer.", "code": "PAYMENT_FAILED"}, 
                                status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Gérer les erreurs de connexion ou autres exceptions
            return Response({"detail": f"Erreur interne du serveur de paiement: {str(e)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)