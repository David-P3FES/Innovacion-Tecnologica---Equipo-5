from django.urls import path
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('post-login/', views.post_login, name='post_login'),
    path('completar-perfil/', views.complete_profile, name='complete_profile'),
]