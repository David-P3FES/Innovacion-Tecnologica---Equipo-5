from django.db import models
from django.contrib.auth.models import User

class Propiedad(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    direccion = models.CharField(max_length=255)

    # Nuevo campo
    tipo_operacion = models.CharField(
        max_length=10,
        choices=[('venta', 'Venta'), ('renta', 'Renta')],
        default='venta'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.tipo_operacion}"

