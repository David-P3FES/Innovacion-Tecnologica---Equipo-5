"""
@file settings.py
@brief Configuración principal del proyecto Django "vivienda".
@details
 Contiene las configuraciones globales del proyecto:
 - Seguridad (SECRET_KEY, DEBUG, ALLOWED_HOSTS).
 - Aplicaciones instaladas (INSTALLED_APPS).
 - Autenticación (Allauth con Google).
 - Middleware.
 - Templates.
 - Base de datos.
 - Archivos estáticos y media.
 - Idioma y zona horaria.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# Rutas base
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# Seguridad
# ==============================
SECRET_KEY = 'django-insecure-=#+e_+@am2c6-+&44b1cauo1ux@d0u*s&39@q-*xqa1c@6+w^7'
DEBUG = True
ALLOWED_HOSTS = ["*", ".elasticbeanstalk.com", "vivienda-env.eba-89uxkyz3.us-west-2.elasticbeanstalk.com"]

# ==============================
# Aplicaciones instaladas
# ==============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'principal',
    'cuentas.apps.CuentasConfig',
    'publicaciones',
    'widget_tweaks',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    "billing",
    
]

SITE_ID = 3

# ==============================
# Autenticación
# ==============================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = 'cuentas:post_login'
LOGOUT_REDIRECT_URL = 'principal:home'

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USERNAME_GENERATOR = 'allauth.account.utils.generate_unique_username'

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
# ==============================
# Middleware
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'cuentas.middleware.RequireCompleteProfileMiddleware',
]

# ==============================
# URLs y WSGI
# ==============================
ROOT_URLCONF = 'vivienda.urls'
WSGI_APPLICATION = 'vivienda.wsgi.application'

# ==============================
# Templates
# ==============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
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

# ==============================
# Base de datos
# ==============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==============================
# Validación de contraseñas
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================
# Internacionalización
# ==============================
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Chihuahua'
USE_I18N = True
USE_TZ = True

# ==============================
# Archivos estáticos y media
# ==============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "cuentas" / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==============================
# Configuración por defecto de campos
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_PRICE_ID_WEEKLY  = os.getenv("STRIPE_PRICE_ID_WEEKLY")
STRIPE_PRICE_ID_MONTHLY = os.getenv("STRIPE_PRICE_ID_MONTHLY")
STRIPE_PRICE_ID_YEARLY  = os.getenv("STRIPE_PRICE_ID_YEARLY")
DOMAIN = os.getenv("DOMAIN")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

LOGIN_URL = '/cuentas/login/'
LOGIN_REDIRECT_URL = '/publicaciones/panel/'
LOGOUT_REDIRECT_URL = '/'

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

SESSION_COOKIE_SAMESITE = "Lax"
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE    = False



#settings....