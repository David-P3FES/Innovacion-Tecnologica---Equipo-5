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

#: Lista de patrones de URL principales del proyecto
urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),  #: Panel de administración de Django

    # Rutas principales (home, resultados)
    path(
        '',
        include('principal.urls')
    ),  #: Incluye las rutas de la app principal

    # Rutas propias de perfil/usuario
    path(
        'cuenta/',
        include('cuentas.urls')
    ),  #: Incluye las rutas personalizadas de la app cuentas

    # Allauth en español
    path(
        'cuenta/',
        include('allauth.urls')
    ),  #: Incluye las rutas de autenticación de Django Allauth
]
