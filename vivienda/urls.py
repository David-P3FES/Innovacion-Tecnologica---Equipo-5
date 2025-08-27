from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas principales (home, resultados)
    path('', include('principal.urls')),

    # Rutas propias de perfil/usuario
    path('cuenta/', include('cuentas.urls')),

    # Allauth en español
    path('cuenta/', include('allauth.urls')),
]
