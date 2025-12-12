import os
from pathlib import Path
from datetime import timedelta

# BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# CONFIG DJANGO
# ----------------------------------------------------

SECRET_KEY = os.getenv('SECRET_KEY', 'change_me_dev_key')
DEBUG = False

ALLOWED_HOSTS = ["*"]

# ----------------------------------------------------
# APPLICATIONS
# ----------------------------------------------------

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tiers
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Apps du projet
    'users',
    'products',
    'orders',
    'ratings',
    'chat',
    'payments',
]

# ----------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------------------------------
# URLS / WSGI
# ----------------------------------------------------

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'


# ----------------------------------------------------
# TEMPLATES
# ----------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ----------------------------------------------------
# DATABASE
# ----------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'terrabia',
        'USER': 'terrabiauser',
        'PASSWORD': 'qKSGcpZ6Vop6pxpOSBWoC5GWQpcUJgcm',
        'HOST': 'postgresql://terrabiauser:qKSGcpZ6Vop6pxpOSBWoC5GWQpcUJgcm@dpg-d4ttfb2dbo4c73aih1t0-a.frankfurt-postgres.render.com/terrabia',
        'PORT': '5432',
    }
}
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('postgresql://terrabiauser:qKSGcpZ6Vop6pxpOSBWoC5GWQpcUJgcm@dpg-d4ttfb2dbo4c73aih1t0-a.frankfurt-postgres.render.com/terrabia')
    )

   # 'default': dj_database_url.parse('postgresql://terrabiauser:qKSGcpZ6Vop6pxpOSBWoC5GWQpcUJgcm@dpg-d4ttfb2dbo4c73aih1t0-a.frankfurt-postgres.render.com/terrabia')
}

# ----------------------------------------------------
# USER MODEL
# ----------------------------------------------------

AUTH_USER_MODEL = 'users.User'

# ----------------------------------------------------
# INTERNATIONALISATION
# ----------------------------------------------------

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Douala'
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------
# STATIC & MEDIA
# ----------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------------------------------
# CORS
# ----------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True

# ----------------------------------------------------
# DRF & JWT
# ----------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
