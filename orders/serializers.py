from rest_framework import serializers
from .models import Commande, LigneCommande, Livraison
from products.serializers import ProduitSerializer
from products.models import Produit
from users.serializers import UserSerializer
# --- Livraison Serializer ---
class LivraisonSerializer(serializers.ModelSerializer):
    agence = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Livraison
        fields = ('id', 'commande', 'agence', 'statut', 'date_creation', 'date_mise_a_jour')
        read_only_fields = ('commande', 'agence', 'date_creation', 'date_mise_a_jour')

# --- Ligne Commande Serializer ---
class LigneCommandeSerializer(serializers.ModelSerializer):
    produit_details = ProduitSerializer(source='produit', read_only=True)
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all(), write_only=True)
    
    class Meta:
        model = LigneCommande
        fields = ("produit", "quantite", "prix_unitaire", "produit_details")
        read_only_fields = ("prix_unitaire", "produit_details")

# --- Commande Serializer ---
class CommandeSerializer(serializers.ModelSerializer):
    lignes = LigneCommandeSerializer(many=True, write_only=True)
    items = LigneCommandeSerializer(source='lignes', many=True, read_only=True)
    acheteur = UserSerializer(read_only=True)
    livraison_statut = serializers.CharField(source='livraison.statut', read_only=True, default=None)
    
    # AJOUT: Accepter adresse_livraison et notes
    adresse_livraison = serializers.CharField(required=True, write_only=True)
    notes = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = Commande
        fields = (
            "id", "acheteur", "total", "statut", "created_at", 
            "items", "lignes", "livraison_statut",
            "adresse_livraison", "notes"
        )
        read_only_fields = ("id", "created_at", "acheteur", "total", "statut")
    
    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes', [])
        adresse_livraison = validated_data.pop('adresse_livraison', '').strip()
        notes = validated_data.pop('notes', '').strip()
        
        if not lignes_data:
            raise serializers.ValidationError("La commande doit contenir au moins un produit")
        
        # Calculer le total
        total = sum(
            ligne['produit'].prix * ligne['quantite'] 
            for ligne in lignes_data
        )
        
        # Créer la commande
        commande = Commande.objects.create(
            acheteur=self.context['request'].user,
            total=total,
            statut='en_attente',
            adresse_livraison=adresse_livraison,
            notes=notes
        )
        
        # Créer les lignes
        for ligne in lignes_data:
            produit = ligne['produit']
            quantite = ligne['quantite']
            
            if quantite <= 0:
                commande.delete()
                raise serializers.ValidationError(
                    f"La quantité pour le produit {produit.nom} doit être > 0"
                )
            
            # Vérifier le stock
            if produit.stock < quantite:
                commande.delete()
                raise serializers.ValidationError(
                    f"Stock insuffisant pour {produit.nom}. Disponible: {produit.stock}"
                )
            
            # Créer la ligne
            LigneCommande.objects.create(
                commande=commande,
                produit=produit,
                quantite=quantite,
                prix_unitaire=produit.prix
            )
            
            # Réduire le stock
            produit.stock -= quantite
            produit.save()
        
        # Créer la livraison associée
        Livraison.objects.create(
            commande=commande,
            statut='en_attente'
        )
        
        return commande