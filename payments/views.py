# payments/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from orders.models import Commande
from products.models import Panier
import uuid
import logging

logger = logging.getLogger(__name__)

class PaymentProcessorView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Log pour debug
        logger.info(f"Payment request data: {request.data}")
        
        # Récupérer les données de la requête
        commande_id = request.data.get('commande_id')
        montant = request.data.get('montant')
        methode = request.data.get('methode')
        numero_telephone = request.data.get('numeroTelephone', '')
        
        # Validation des données
        if not commande_id:
            return Response(
                {
                    "success": False, 
                    "message": "commande_id requis",
                    "transaction_id": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not montant:
            return Response(
                {
                    "success": False, 
                    "message": "montant requis",
                    "transaction_id": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not methode:
            return Response(
                {
                    "success": False, 
                    "message": "methode requise",
                    "transaction_id": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier que la commande existe et appartient à l'utilisateur
        try:
            commande = Commande.objects.get(id=commande_id, acheteur=request.user)
        except Commande.DoesNotExist:
            return Response(
                {
                    "success": False, 
                    "message": "Commande introuvable",
                    "transaction_id": ""
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier que le montant correspond
        try:
            montant_float = float(montant)
            total_float = float(commande.total)
            
            if abs(montant_float - total_float) > 0.01:  # Tolérance pour les arrondis
                return Response(
                    {
                        "success": False, 
                        "message": f"Montant incorrect. Attendu: {commande.total}, Reçu: {montant}",
                        "transaction_id": ""
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {
                    "success": False, 
                    "message": "Montant invalide",
                    "transaction_id": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validation spécifique selon la méthode
        if methode == "mobile_money":
            if not numero_telephone:
                return Response(
                    {
                        "success": False, 
                        "message": "Numéro de téléphone requis pour Mobile Money",
                        "transaction_id": ""
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            # TODO: Valider le format du numéro
            # TODO: Appeler l'API Mobile Money (MTN, Orange, etc.)
            logger.info(f"Processing Mobile Money payment: {numero_telephone}")
            payment_success = True  # Simulé pour l'instant
            
        elif methode == "carte":
            # TODO: Intégrer un processeur de paiement par carte
            logger.info("Processing card payment")
            payment_success = True  # Simulé pour l'instant
            
        elif methode == "especes":
            # Paiement à la livraison - toujours accepté
            logger.info("Payment on delivery")
            payment_success = True
            
        else:
            return Response(
                {
                    "success": False, 
                    "message": f"Méthode de paiement invalide: {methode}",
                    "transaction_id": ""
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Traiter le paiement
        if payment_success:
            # Mettre à jour le statut de la commande
            if methode == "especes":
                commande.statut = 'en_attente_paiement'
                message = "Commande confirmée. Paiement à la livraison."
            else:
                commande.statut = 'confirmee'
                message = "Paiement effectué avec succès"
            
            commande.save()
            
            # Générer un ID de transaction unique
            transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            
            # Vider le panier de l'utilisateur
            try:
                deleted_count = Panier.objects.filter(acheteur=request.user).delete()
                logger.info(f"Deleted {deleted_count[0]} items from cart")
            except Exception as e:
                logger.error(f"Error clearing cart: {e}")
            
            logger.info(f"Payment successful. Transaction ID: {transaction_id}")
            
            return Response(
                {
                    "success": True,
                    "transaction_id": transaction_id,
                    "message": message
                },
                status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    "success": False,
                    "transaction_id": "",
                    "message": "Échec du paiement. Veuillez réessayer."
                },
                status=status.HTTP_400_BAD_REQUEST
            )