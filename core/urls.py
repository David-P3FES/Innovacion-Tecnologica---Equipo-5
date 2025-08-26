from django.urls import path, include
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.home, name='home'),
    path('resultados/', views.resultados_busqueda, name='resultados_busqueda'),
    path('propiedad/<int:id>/', views.detalle_propiedad, name='detalle_propiedad'),
    path('cuenta/', views.registro_login, name='registro_login'),
    path('planes-precios/', views.planes_precios, name='planes_precios'),

    # Privadas - Comprador/Rentador
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/completar/', views.completar_perfil, name='completar_perfil'),
    path('lista-deseos/', views.lista_deseos, name='lista_deseos'),

    # Privadas - Vendedor
    path('vendedor/', views.panel_vendedor, name='panel_vendedor'),
    path('vendedor/nueva/', views.nueva_publicacion, name='nueva_publicacion'),
    path('vendedor/editar/<int:id>/', views.edicion_publicacion, name='edicion_publicacion'),
    path('vendedor/historial/', views.historial_publicaciones, name='historial_publicaciones'),

    # Privadas - Administrador
    path('admin-panel/', views.panel_administracion, name='panel_administracion'),

    # Allauth
    path('accounts/', include('allauth.urls')),
]
