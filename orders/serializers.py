from rest_framework import serializers
from .models import Commande, LigneCommande, Livraison
from products.serializers import ProduitSerializer # Assurez-vous que ceci est importé/existe
from products.models import Produit

# --- 1. Livraison Serializer (Nécessaire pour DeliveryViewSet) ---
class LivraisonSerializer(serializers.ModelSerializer):
    # Afficher le nom d'utilisateur de l'agence
    agence = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Livraison
        fields = ('id', 'commande', 'agence', 'statut', 'date_creation', 'date_mise_a_jour')
        read_only_fields = ('commande', 'agence', 'date_creation', 'date_mise_a_jour')

# --- 2. Ligne Commande Serializer ---
class LigneCommandeSerializer(serializers.ModelSerializer):
    # ... (Le code existant)
    # Pour l'affichage, vous voudrez probablement voir les détails du produit
    produit_details = ProduitSerializer(source='produit', read_only=True) 
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all(), write_only=True)

    class Meta:
        model = LigneCommande
        fields = ("produit","quantite","prix_unitaire", "produit_details") # Ajout produit_details
        read_only_fields = ("prix_unitaire", "produit_details")

# --- 3. Commande Serializer (Amélioré pour l'historique) ---
class CommandeSerializer(serializers.ModelSerializer):
    # Lignes utilisées pour la CREATION (write_only)
    lignes = LigneCommandeSerializer(many=True, write_only=True)
    # Lignes utilisées pour l'AFFICHAGE (read_only)
    items = LigneCommandeSerializer(source='lignes', many=True, read_only=True) 
    
    acheteur = serializers.StringRelatedField(read_only=True)
    
    # Afficher le statut de livraison directement dans la commande
    livraison_statut = serializers.CharField(source='livraison.statut', read_only=True) 

    class Meta:
        model = Commande
        fields = ("id","acheteur","total","statut","created_at","items","lignes", "livraison_statut")
        read_only_fields = ("id","created_at","acheteur","total", "statut") # Le statut est géré par la logique métier/livraison

    # ... (La méthode create() existante est parfaite, pas besoin de la modifier)