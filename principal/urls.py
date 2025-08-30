"""
@file urls.py
@brief Rutas de la aplicación `principal`.
@details Define las URLs que conectan las vistas principales del sitio:
         - Página de inicio.
         - Resultados de búsqueda de propiedades.
"""

from django.urls import path
from . import views
from . import views as principal_views

#: Namespace de la app `principal` para diferenciar sus rutas
app_name = "principal"  

#: Lista de patrones de URL de la app `principal`
urlpatterns = [
    path(
        '', 
        views.home, 
        name='home'
    ),  #: Página principal (vista home)

    path(
        'resultados/', 
        views.resultados_busqueda, 
        name='resultados_busqueda'
    ),  #: Página de resultados de búsqueda de propiedades

    path("me-encantas/", principal_views.mis_favoritos, name="mis_favoritos"),
    path("fav/toggle/<int:pk>/", views.toggle_favorito, name="toggle_favorito"),
]

