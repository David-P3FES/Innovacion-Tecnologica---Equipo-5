from django.urls import path, include
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.home, name='home'),
    path('resultados/', views.resultados_busqueda, name='resultados_busqueda'),
    path('propiedad/<int:id>/', views.detalle_propiedad, name='detalle_propiedad'),
    path('planes-precios/', views.planes_precios, name='planes_precios'),
    path('lista-deseos/', views.lista_deseos, name='lista_deseos'),
    path('accounts/', include('allauth.urls')),
]
