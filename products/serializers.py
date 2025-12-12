from rest_framework import serializers
from .models import Produit, Panier

class ProduitSerializer(serializers.ModelSerializer):
    agriculteur = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Produit
        fields = "__all__"
        read_only_fields = ("id","agriculteur","created_at")

class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        fields = "__all__"
        read_only_fields = ("id",)
