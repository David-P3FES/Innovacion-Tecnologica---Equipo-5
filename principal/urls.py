from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resultados/', views.resultados_busqueda, name='resultados_busqueda'),

]
