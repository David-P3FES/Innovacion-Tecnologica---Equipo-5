"""
@file apps.py
@brief Configuración de la aplicación `cuentas` en Django.
@details
 Este archivo define la clase de configuración para la app `cuentas`,
 utilizada por Django para registrar e inicializar la aplicación en el proyecto.
"""

from django.apps import AppConfig


class CuentasConfig(AppConfig):
    """
    @class CuentasConfig
    @brief Clase de configuración para la aplicación `cuentas`.
    @details
     - `default_auto_field`: especifica el tipo de campo automático por defecto 
       para las claves primarias (en este caso `BigAutoField`).
     - `name`: nombre interno de la app que Django usará en el proyecto.
    """
    default_auto_field = 'django.db.models.BigAutoField'  #: Campo auto por defecto
    name = 'cuentas'  #: Nombre de la aplicación
