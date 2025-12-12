from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Champ de confirmation du mot de passe (non mappé au modèle)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'role', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # Validation que les deux mots de passe correspondent
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return data

    def create(self, validated_data):
        # Création de l'utilisateur avec un mot de passe hashé
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role=validated_data.get('role', 'acheteur'), # Définit 'acheteur' si non fourni
            phone=validated_data.get('phone', None)
        )
        return user