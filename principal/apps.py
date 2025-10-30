"""
@file apps.py
@brief Configuración de la aplicación `principal` en Django.
@details
 Este archivo define la clase de configuración para la app `principal`,
 utilizada por Django para registrar e inicializar la aplicación en el proyecto.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    @class CoreConfig
    @brief Clase de configuración para la aplicación `principal`.
    @details
     - `default_auto_field`: especifica el tipo de campo automático por defecto 
       para las claves primarias (en este caso `BigAutoField`).
     - `name`: nombre interno de la app dentro del proyecto.
    """
    default_auto_field = 'django.db.models.BigAutoField'  #: Campo auto por defecto
    name = 'principal'  #: Nombre de la aplicación
