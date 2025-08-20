from django.contrib import admin
from django.urls import path, include
from core.views import cuenta_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    
    # Este debe ir antes
    path('cuenta/', cuenta_redirect),  # Redirecciona a /cuenta/login/

    # Luego se incluyen las URLs de django-allauth
    path('cuenta/', include('allauth.urls')),
]