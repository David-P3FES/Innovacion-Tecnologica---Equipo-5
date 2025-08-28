"""
@file models.py
@brief Modelos y validadores de la aplicación `cuentas`.
@details
 Contiene:
  - Validadores para RFC y número de WhatsApp.
  - Modelo `Perfil` asociado a cada usuario.
  - Señal para crear automáticamente un perfil al registrar un usuario.
  - Función helper para comprobar si un perfil está incompleto.
"""

from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# ============================
# Validadores
# ============================

#: Expresión regular para validar RFC (personas o empresas, en mayúsculas)
RFC_REGEX = r'^([A-ZÑ&]{3}\d{6}[A-Z0-9]{3}|[A-ZÑ&]{4}\d{6}[A-Z0-9]{3})$'

#: Validador de RFC con mensaje de error personalizado
rfc_validator = RegexValidator(
    regex=RFC_REGEX,
    message='RFC inválido. Ejemplo persona: GODE561231GR8 / empresa: ABC001231AB1 (usar MAYÚSCULAS).'
)

#: Expresión regular para validar números telefónicos (10 dígitos o formato internacional +521)
PHONE_REGEX = r'^(\+?52)?1?\d{10}$'

#: Validador de número de WhatsApp con mensaje de error personalizado
phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message='Número inválido. Usa 10 dígitos (ej. 6561234567) o formato +5216561234567.'
)

# ============================
# Modelo Perfil
# ============================

class Perfil(models.Model):
    """
    @class Perfil
    @brief Modelo que extiende la información del usuario con datos adicionales.
    @details
     Requisitos para considerar el perfil como completo:
      - `user.username`, `first_name`, `last_name`, `email`
      - RFC válido y único
      - Número de WhatsApp válido
    """

    #: Relación uno a uno con el modelo de usuario
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    #: RFC del usuario (único, opcional, validado por `rfc_validator`)
    rfc = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        validators=[rfc_validator]
    )

    #: Número de WhatsApp del usuario (opcional, validado por `phone_validator`)
    whatsapp = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=[phone_validator]
    )

    def __str__(self):
        """
        @brief Representación en texto del perfil.
        @return Cadena con el username del usuario.
        """
        return f'Perfil de {self.user.username}'

    def is_complete(self) -> bool:
        """
        @brief Verifica si el perfil está completo.
        @details Comprueba que los campos requeridos de `User` y `Perfil` estén presentes.
        @return True si el perfil contiene todos los datos obligatorios, False en caso contrario.
        """
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
    """
    @brief Crea automáticamente un objeto Perfil al registrar un nuevo usuario.
    @param sender Modelo que envía la señal (User).
    @param instance Instancia de usuario creada o actualizada.
    @param created Booleano que indica si el usuario fue creado.
    @param kwargs Argumentos adicionales de la señal.
    """
    if created:
        Perfil.objects.get_or_create(user=instance)


# ============================
# Helper de compatibilidad
# ============================

def perfil_incompleto(user) -> bool:
    """
    @brief Comprueba si un usuario tiene un perfil incompleto.
    @param user Instancia de usuario a validar.
    @return True si el perfil no existe o está incompleto, False si está completo.
    """
    try:
        return not user.perfil.is_complete()
    except Perfil.DoesNotExist:
        return True
