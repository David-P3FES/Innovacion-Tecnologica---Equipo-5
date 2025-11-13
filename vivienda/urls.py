"""
@file urls.py
@brief Enrutador principal del proyecto Django "vivienda".
@details
 Define las rutas globales del proyecto:
 - Panel de administración de Django.
 - Rutas de la aplicación `principal`.
 - Rutas de la aplicación `cuentas`.
 - Rutas de la aplicación `publicaciones`.
 - Rutas de autenticación social con Allauth.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Página principal
    path('', include('principal.urls')),

    # Cuentas (tu app)
    path('cuentas/', include(('cuentas.urls', 'cuentas'), namespace='cuentas')),

    # Allauth (Google, email, etc.)
    path('auth/', include('allauth.urls')),

    # Publicaciones
    path('publicaciones/', include('publicaciones.urls')),

    # Billing / Stripe
    path('billing/', include('billing.urls')),
]


# Servir archivos MEDIA y STATIC tanto en desarrollo como producción (Elastic Beanstalk Single Instance)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)