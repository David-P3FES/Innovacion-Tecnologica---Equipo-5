from django.conf import settings    
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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