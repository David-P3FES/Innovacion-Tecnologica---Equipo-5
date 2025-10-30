"""
@file wsgi.py
@brief Configuración WSGI para el proyecto Vivienda.
@details
 Expone la aplicación WSGI como una variable de nivel de módulo llamada `application`.
 Es utilizada por servidores como Gunicorn o uWSGI para desplegar la aplicación en producción.

@see https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

#: Configuración por defecto del módulo de settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivienda.settings')

#: Objeto WSGI callable utilizado por servidores (ej. Gunicorn, uWSGI)
application = get_wsgi_application()
