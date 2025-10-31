"""
@file urls.py
@brief Definición de las rutas de la aplicación `cuentas`.
@details
 Contiene las URL relacionadas con la gestión de perfiles de usuario:
  - Redirección post login
  - Completar perfil
  - Ver perfil
  - Editar perfil
  - Rutas de autenticación (login, logout, registro) mediante django-allauth
"""

from django.urls import path, include
from . import views

#: Nombre de la aplicación para namespacing de URLs
app_name = 'cuentas'

#: Rutas de la aplicación `cuentas`
urlpatterns = [
    path(
        'post-login/',
        views.post_login,
        name='post_login'
    ),  #: Vista para manejar la redirección después de iniciar sesión

    path(
        'completar-perfil/',
        views.complete_profile,
        name='complete_profile'
    ),  #: Vista para completar el perfil del usuario

    path(
        "perfil/",
        views.ver_perfil,
        name="ver_perfil"
    ),  #: Vista para mostrar el perfil del usuario

    path(
        "perfil/editar/",
        views.editar_perfil,
        name="editar_perfil"
    ),  #: Vista para editar los datos del perfil

    # ✅ Aquí agregas las rutas de django-allauth
    path("", include("allauth.urls")),
]
