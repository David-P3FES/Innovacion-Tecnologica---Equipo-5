from django.urls import path
from . import views

urlpatterns = [
    # Privadas - Comprador/Rentador
    path('perfil/completar/', views.completar_perfil, name='completar_perfil'),

    # Privadas - Administrador
    #path('admin-panel/', views.panel_administracion, name='panel_administracion'),

    # Redirección de cuenta
    path('redirect/', views.cuenta_redirect, name='cuenta_redirect'),
]
