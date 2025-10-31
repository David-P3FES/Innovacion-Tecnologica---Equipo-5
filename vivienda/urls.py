"""
@file urls.py
@brief Enrutador principal del proyecto Django "vivienda".
@details
Define las rutas globales del proyecto:
- Panel de administración de Django.
- Rutas de la aplicación `principal` (inicio y resultados).
- Rutas de la aplicación `cuentas` (perfil y usuario).
- Rutas de autenticación social con Allauth.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, path

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        include('principal.urls')
    ),
    path(
        'cuenta/',
        include('cuentas.urls')
    ),

    path(
        'cuenta/',
        include('allauth.urls')
    ),
    path("publicaciones/", include("publicaciones.urls")),

    path(
        '',
        include('principal.urls')
    ),

    path(
        'cuenta/',
        include('allauth.urls')
    ),

    path("publicaciones/", include("publicaciones.urls")),

    path("billing/", include("billing.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)