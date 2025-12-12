from rest_framework import serializers
from .models import Notation
from users.models import User

class RatingSerializer(serializers.ModelSerializer):
    # L'agriculteur peut être passé par ID ou par nom d'utilisateur dans la requête
    agriculteur_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='agriculteur'),
        source='agriculteur',
        write_only=True
    )
    
    # Afficher le nom de l'agriculteur en lecture seule
    agriculteur_username = serializers.CharField(source='agriculteur.username', read_only=True)

    class Meta:
        model = Notation
        fields = ('id', 'agriculteur_id', 'agriculteur_username', 'note', 'commentaire', 'created_at')
        read_only_fields = ('id', 'created_at', 'agriculteur_username')
        extra_kwargs = {
            # L'acheteur est automatiquement défini par la vue
            'acheteur': {'read_only': True} 
        }