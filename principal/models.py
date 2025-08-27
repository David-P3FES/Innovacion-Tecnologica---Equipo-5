from django.db import models
from django.contrib.auth.models import User

class Propiedad(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    tipo_operacion = models.CharField(max_length=50)  # renta/venta
    estado = models.CharField(max_length=50, default='disponible')

    def __str__(self):
        return self.titulo
