from rest_framework import serializers
from .models import Commande, LigneCommande, Livraison
from products.serializers import ProduitSerializer
from products.models import Produit

class LigneCommandeSerializer(serializers.ModelSerializer):
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all())

    class Meta:
        model = LigneCommande
        fields = ("produit","quantite","prix_unitaire")

class CommandeSerializer(serializers.ModelSerializer):
    lignes = LigneCommandeSerializer(many=True, write_only=True)
    acheteur = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Commande
        fields = ("id","acheteur","total","statut","created_at","lignes")
        read_only_fields = ("id","created_at","acheteur","total")

    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes')
        user = self.context['request'].user
        # compute total and create Commande + LigneCommande atomically
        from django.db import transaction
        total = 0
        with transaction.atomic():
            commande = Commande.objects.create(acheteur=user, total=0, **validated_data)
            for l in lignes_data:
                produit = l['produit']
                quantite = l['quantite']
                if produit.stock < quantite:
                    raise serializers.ValidationError(f"Stock insuffisant pour {produit.nom}")
                prix_unitaire = produit.prix
                total += prix_unitaire * quantite
                # decrement stock
                produit.stock -= quantite
                produit.save()
                LigneCommande.objects.create(commande=commande, produit=produit, quantite=quantite, prix_unitaire=prix_unitaire)
            commande.total = total
            commande.save()
        return commande
