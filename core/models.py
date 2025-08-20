from django.conf import settings    
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Modelo para las propiedades
# Añadido el campo tipo_operacion para distinguir entre venta y renta
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

class Perfil(models.Model):
    ROL_CHOICES = [
        ('comprador', 'Comprador/Rentador'),
        ('vendedor', 'Vendedor/Inmobiliaria'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    rfc = models.CharField(max_length=13, blank=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, blank=True)

    telefono = models.CharField(max_length=20, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_automatico(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

def perfil_incompleto(user):
    try:
        p = user.perfil
        return (not p.rfc) or (not p.rol)
    except Perfil.DoesNotExist:
        return True