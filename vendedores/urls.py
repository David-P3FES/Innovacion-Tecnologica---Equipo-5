from django.urls import path
from . import views

urlpatterns = [
    
    path('editar/<int:id>/', views.edicion_publicacion, name='editar'), 
    path('historial/', views.historial_publicaciones, name='historial'),
    path('publicar/', views.nueva_publicacion, name='publicar'),  
    path('panel/', views.panel_vendedor, name='historial'), 
    
]