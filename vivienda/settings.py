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

# ==============================
# Rutas base
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# Seguridad
# ==============================
SECRET_KEY = 'django-insecure-=#+e_+@am2c6-+&44b1cauo1ux@d0u*s&39@q-*xqa1c@6+w^7'  #: Clave secreta del proyecto
DEBUG = True  #: Modo debug (True en desarrollo, False en producción)
ALLOWED_HOSTS = []  #: Hosts permitidos

# ==============================
# Aplicaciones instaladas
# ==============================
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps personalizadas
    'principal',
    'cuentas.apps.CuentasConfig',   # registra señales

    # Utilidades
    'widget_tweaks',

    # Autenticación (Allauth)
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 3  #: ID del sitio para django.contrib.sites

# ==============================
# Autenticación
# ==============================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = 'cuentas:post_login'  #: Redirección tras login
LOGOUT_REDIRECT_URL = 'principal:home'     #: Redirección tras logout

# Configuración de Allauth
ACCOUNT_AUTHENTICATION_METHOD = "email"   #: Login solo con email
ACCOUNT_USERNAME_REQUIRED = False         #: Username no requerido
ACCOUNT_EMAIL_REQUIRED = True             #: Email obligatorio
ACCOUNT_UNIQUE_EMAIL = True               #: Emails únicos
ACCOUNT_EMAIL_VERIFICATION = "none"       #: Sin verificación en desarrollo
ACCOUNT_USERNAME_GENERATOR = 'allauth.account.utils.generate_unique_username'

# Flujo social
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True   #: Crea usuario local sin pedir datos extra

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
                'django.template.context_processors.request',   # necesario para allauth
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
LANGUAGE_CODE = 'es-mx'         #: Idioma principal
TIME_ZONE = 'America/Chihuahua' #: Zona horaria local
USE_I18N = True
USE_TZ = True

# ==============================
# Archivos estáticos y media
# ==============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "cuentas" / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==============================
# Configuración por defecto de campos
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
