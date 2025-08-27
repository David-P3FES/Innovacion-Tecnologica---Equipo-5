from pathlib import Path
import os

# 📁 BASE_DIR define la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# 🚨 Llave secreta para firmar cookies, tokens, etc. (¡No compartir en producción!)
SECRET_KEY = 'django-insecure-=#+e_+@am2c6-+&44b1cauo1ux@d0u*s&39@q-*xqa1c@6+w^7'

# 🛠️ Modo debug (muestra errores si hay fallas)
DEBUG = True

# 🌍 Dominios permitidos para acceder a la app (vacío en desarrollo)
ALLOWED_HOSTS = []

# 🧩 Aplicaciones instaladas (apps que usas)
INSTALLED_APPS = [
    'django.contrib.admin',          # Admin de Django
    'django.contrib.auth',           # Sistema de autenticación
    'django.contrib.contenttypes',   # Tipos de contenido
    'django.contrib.sessions',       # Manejo de sesiones
    'django.contrib.messages',       # Mensajes flash (notificaciones)
    'django.contrib.staticfiles',    # Archivos estáticos (CSS, JS)
    'cuentas',                          # Tu app principal personalizada
    'principal',
    "widget_tweaks",

    # Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 2

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True



# Allauth básico
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_REDIRECT_URL = 'completar_perfil'  # en cuanto se registre, lo mandamos a completar perfil

# 🧱 Middleware (procesos que se ejecutan en cada petición)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',         # Protección contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

#  requerido por allauth
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

# 🔗 Archivo principal de rutas del proyecto
ROOT_URLCONF = 'vivienda.urls'

# 📄 Configuración de plantillas HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necesario para django-allauth y formularios
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🚀 Punto de entrada WSGI para servidores en producción
WSGI_APPLICATION = 'vivienda.wsgi.application'

# 🗃️ Configuración de base de datos (SQLite para desarrollo)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 Validadores de contraseñas (recomendados para seguridad)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌎 Internacionalización y zona horaria
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Chihuahua'
USE_I18N = True
USE_TZ = True

# 🖼️ Archivos estáticos (CSS, JS, imágenes de diseño)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "cuentas" / "static",
]

# 🧾 Archivos subidos por los usuarios (como imágenes)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 🔢 Tipo de campo por defecto para primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
