from django.db import models
from django.contrib.auth.models import User   # ✅ import correcto

class Propiedad(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    direccion = models.CharField(max_length=255)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ ya no truena
    estado = models.CharField(
        max_length=20,
        choices=[
            ('disponible', 'Disponible'),
            ('en_trato', 'En trato'),
            ('vendido', 'Vendido')
        ],
        default='disponible'
    )
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
