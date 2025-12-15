# serializers.py
from rest_framework import serializers
from .models import Produit, Panier

class ProduitSerializer(serializers.ModelSerializer):
    agriculteur_nom = serializers.CharField(source='agriculteur.username', read_only=True)
    agriculteur_id = serializers.IntegerField(source='agriculteur.id', read_only=True)
    
    class Meta:
        model = Produit
        fields = ['id', 'nom', 'description', 'prix', 'stock', 'categorie', 
                  'unite', 'image', 'agriculteur_id', 'agriculteur_nom', 'created_at']
        read_only_fields = ['id', 'agriculteur_id', 'agriculteur_nom', 'created_at']

class PanierSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)  # inclut les détails du produit

    class Meta:
        model = Panier
        fields = '__all__'



