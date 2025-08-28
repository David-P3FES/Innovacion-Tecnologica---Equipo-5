from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# ============================
# Validadores
# ============================

RFC_REGEX = r'^([A-ZÑ&]{3}\d{6}[A-Z0-9]{3}|[A-ZÑ&]{4}\d{6}[A-Z0-9]{3})$'
rfc_validator = RegexValidator(
    regex=RFC_REGEX,
    message='RFC inválido. Ejemplo persona: GODE561231GR8 / empresa: ABC001231AB1 (usar MAYÚSCULAS).'
)

PHONE_REGEX = r'^(\+?52)?1?\d{10}$'
phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message='Número inválido. Usa 10 dígitos (ej. 6561234567) o formato +5216561234567.'
)

# ============================
# Modelo Perfil
# ============================

class Perfil(models.Model):
    """
    Perfil de usuario para publicar/rentar.
    Requisitos de "perfil completo":
      - user.username, first_name, last_name, email
      - rfc válido y único
      - whatsapp válido
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    rfc = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        validators=[rfc_validator]
    )

    whatsapp = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[phone_validator]
    )

    def __str__(self):
        return f'Perfil de {self.user.username}'

    def is_complete(self) -> bool:
        """Comprueba si el perfil está completo"""
        u = self.user
        base_ok = all([
            bool(u.username and u.username.strip()),
            bool(u.first_name and u.first_name.strip()),
            bool(u.last_name and u.last_name.strip()),
            bool(u.email and u.email.strip()),
        ])
        extra_ok = all([
            bool(self.rfc and str(self.rfc).strip()),
            bool(self.whatsapp and str(self.whatsapp).strip()),
        ])
        return base_ok and extra_ok


# ============================
# Señal: crear Perfil automático
# ============================

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_automatico(sender, instance, created, **kwargs):
    """Crea el Perfil automáticamente al registrar un User"""
    if created:
        Perfil.objects.get_or_create(user=instance)


# ============================
# Helper de compatibilidad
# ============================

def perfil_incompleto(user) -> bool:
    """Devuelve True si el perfil está incompleto"""
    try:
        return not user.perfil.is_complete()
    except Perfil.DoesNotExist:
        return True
