"""
@file asgi.py
@brief Configuración ASGI para el proyecto Vivienda.
@details
 Expone la aplicación ASGI como una variable de nivel de módulo llamada `application`.
 Se utiliza para manejar conexiones asíncronas (WebSockets, HTTP/2, etc.) en despliegues compatibles.

@see https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

#: Configuración por defecto del módulo de settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivienda.settings')

#: Objeto ASGI callable utilizado por servidores compatibles (ej. Daphne, Uvicorn).
application = get_asgi_application()
