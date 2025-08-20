from django.contrib import admin
from django.urls import path, include

print(">>CARGANDO ESTE URS.PY DEL PROYECTO")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cuenta/', include('allauth.urls')),  # <-- Rutas de login/registro
]
