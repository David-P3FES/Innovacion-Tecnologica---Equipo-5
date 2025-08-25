from django.urls import path, include
from . import views

urlpatterns = [
    
 
    path('cuenta/', views.registro_login, name='registro_login'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/completar/', views.completar_perfil, name='completar_perfil'),
]