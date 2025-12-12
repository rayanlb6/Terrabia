from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # change in prod: IsAdminUser for list/create?

    def get_permissions(self):
        if self.action in ['create', 'register']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
