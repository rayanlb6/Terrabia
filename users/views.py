from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from .models import User
from rest_framework import viewsets # Pour UserViewSet

# --- VueSet Standard ---
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs (principalement utilisé par l'Admin).
    """
    queryset = User.objects.all()
    # Le serializer doit être créé dans users/serializers.py
    serializer_class = UserRegistrationSerializer 
    permission_classes = [permissions.IsAdminUser] # Restreindre l'accès par défaut

# --- Vue d'Inscription Personnalisée ---
class UserRegistrationView(generics.CreateAPIView):
    """
    Gère l'inscription d'un nouvel utilisateur.
    URL: POST /api/auth/register/
    """
    queryset = User.objects.all()
    # Utiliser le même serializer, mais sans exiger l'authentification
    serializer_class = UserRegistrationSerializer 
    permission_classes = [permissions.AllowAny] # Permet à tout le monde de s'inscrire

    # Optionnel: Vous pouvez surcharger la méthode pour renvoyer le token après inscription
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Vous pouvez renvoyer une réponse personnalisée ici, par exemple en incluant un token
        return Response({
            "user": UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
            "message": "Inscription réussie. Connectez-vous."
        }, status=status.HTTP_201_CREATED)