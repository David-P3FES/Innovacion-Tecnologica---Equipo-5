"""
@file models.py
@brief Modelos de la aplicación `principal`.
@details Contiene las definiciones de base de datos para las propiedades
         registradas por los usuarios (vendedores).
"""

from django.db import models
from django.contrib.auth.models import User


class Propiedad(models.Model):
    """
    @class Propiedad
    @brief Modelo que representa una propiedad publicada.
    @details
     - Relacionada a un `User` (vendedor).
     - Incluye título, dirección, tipo de operación (renta/venta) y estado.
    """

    vendedor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Usuario vendedor al que pertenece la propiedad."
    )  #: Relación con el usuario vendedor

    titulo = models.CharField(
        max_length=255,
        help_text="Título descriptivo de la propiedad."
    )  #: Título de la propiedad

    direccion = models.CharField(
        max_length=255,
        help_text="Dirección de la propiedad."
    )  #: Dirección física de la propiedad

    tipo_operacion = models.CharField(
        max_length=50,
        help_text="Tipo de operación: renta o venta."
    )  #: Tipo de operación

    estado = models.CharField(
        max_length=50,
        default='disponible',
        help_text="Estado de la propiedad (ej. disponible, en trato, vendida)."
    )  #: Estado actual de la propiedad

    def __str__(self):
        """
        @brief Devuelve representación en texto de la propiedad.
        @return Título de la propiedad.
        """
        return self.titulo
