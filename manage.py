"""
@file manage.py
@brief Utilidad de línea de comandos para tareas administrativas de Django.
@details
 Este archivo permite ejecutar comandos de administración de Django como:
 - `runserver` para iniciar el servidor de desarrollo.
 - `migrate` para aplicar migraciones a la base de datos.
 - `createsuperuser` para crear usuarios administradores.
 - Otros comandos disponibles a través de `django.core.management`.

 Generalmente no se modifica, ya que lo genera Django automáticamente al crear el proyecto.
"""

#!/usr/bin/env python
import os
import sys


def main():
    """
    @brief Ejecuta las tareas administrativas de Django.
    @details
     - Configura la variable de entorno `DJANGO_SETTINGS_MODULE` con `vivienda.settings`.
     - Ejecuta el comando recibido en la terminal (ej. runserver, makemigrations).
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vivienda.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
