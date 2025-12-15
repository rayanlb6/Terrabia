from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from users.views import AuthMeView

# Importations des Views
# Note: Nous supposons que ces vues existent dans les fichiers appropriés.
from users.views import UserViewSet, UserRegistrationView # Ajout de UserRegistrationView
from products.views import ProduitViewSet, PanierViewSet
from orders.views import CommandeViewSet, DeliveryViewSet # Ajout de DeliveryViewSet (nécessaire pour /deliveries/accept)
from ratings.views import RatingViewSet # Ajout d'un ViewSet pour les notations
from chat.views import MessageViewSet # Ajout d'un ViewSet pour le chat
from payments.views import PaymentProcessorView # Ajout d'une vue pour le paiement

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# --- 1. ROUTERS DRF (Pour les CRUD standards) ---
router = routers.DefaultRouter()
# Le ViewSet User est souvent pour les actions d'admin ou de profil
router.register(r'users', UserViewSet) 
router.register(r'products', ProduitViewSet, basename='produit') # Liste produits, Ajout produits (CRUD)
router.register(r'cart', PanierViewSet, basename='panier') # Panier (CRUD et action 'add')
router.register(r'orders', CommandeViewSet, basename='commande') # Commandes (CRUD et action 'history', 'create' si nécessaire)
router.register(r'ratings', RatingViewSet, basename='rating') # Notations (CRUD ou seulement POST)
router.register(r'messages', MessageViewSet, basename='message') # Messages (Historique GET)
router.register(r'deliveries', DeliveryViewSet, basename='delivery') # Livraisons (pour l'action 'accept')


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # --- 2. AUTHENTIFICATION (Standard + Custom) ---
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # POST /api/auth/register/ (Ajouté)
    path('api/auth/register/', UserRegistrationView.as_view(), name='register'),
    path('api/auth/me/', AuthMeView.as_view(), name='auth_me'),

    # --- 3. URLS GÉRÉES PAR LE ROUTER (products/, cart/, orders/, ratings/, messages/, deliveries/) ---
    path('api/', include(router.urls)), 
    
    # --- 4. ACTIONS SPÉCIFIQUES NON GÉRÉES PAR LE ROUTER ---
    
    # POST /api/payments/process/ (Ajouté)
    # Ceci est souvent une vue APIView simple car il n'est pas lié à un ViewSet
    path('api/payments/process/', PaymentProcessorView.as_view(), name='process_payment'),
]

# Servir les fichiers médias (images des produits) en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)