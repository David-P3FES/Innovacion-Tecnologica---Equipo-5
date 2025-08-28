"""
@file admin.py
@brief Configuración del panel de administración de Django para el modelo de usuario.
@details
 Este archivo importa el modelo de usuario definido en el proyecto (CustomUser si existe)
 mediante la función `get_user_model()`. Esto permite extender o personalizar el modelo
 en caso de que se haya sobrescrito en lugar de usar el modelo User por defecto.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model

#: Obtiene el modelo de usuario activo (CustomUser o el User por defecto de Django)
User = get_user_model()
