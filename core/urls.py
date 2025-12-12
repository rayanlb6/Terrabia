from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import UserViewSet
from products.views import ProduitViewSet, PanierViewSet
from orders.views import CommandeViewSet
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProduitViewSet, basename='produit')
router.register(r'cart', PanierViewSet, basename='panier')
router.register(r'orders', CommandeViewSet, basename='commande')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    # apps-specific urls if needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
