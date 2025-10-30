"""
@file models.py
@brief Modelos y validadores de la aplicación `cuentas`.
@details
 Contiene:
  - Validadores para RFC y número de WhatsApp.
  - Modelo `Perfil` asociado a cada usuario.
  - Señal para crear automáticamente un perfil al registrar un usuario.
  - Función helper para comprobar si un perfil está incompleto.
  - Integración lista para Stripe (customer/subscription/price + helpers).
"""

from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Intentar importar stripe de forma opcional
try:
    import stripe  # type: ignore
except Exception:  # pragma: no cover
    stripe = None

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

    # -----------------------------------------------------------------------------
    # Stripe: nuevos campos y helpers
    # -----------------------------------------------------------------------------

    #: Bandera legacy (se mantiene para compatibilidad con vistas/plantillas)
    is_subscribed = models.BooleanField(
        default=False,
        help_text="Compatibilidad: indica si se detecta una suscripción activa (se sincroniza desde Stripe)."
    )

    #: ID del Customer en Stripe (p.ej. 'cus_ABC123')
    stripe_customer_id = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )

    #: ID de la suscripción activa en Stripe (p.ej. 'sub_ABC123')
    stripe_subscription_id = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )

    #: ID del precio (Price) usado en la suscripción (p.ej. 'price_ABC123')
    stripe_price_id = models.CharField(
        max_length=255, null=True, blank=True
    )

    #: Estado textual de la suscripción en Stripe
    STRIPE_STATUS_CHOICES = [
        ("incomplete", "incomplete"),
        ("incomplete_expired", "incomplete_expired"),
        ("trialing", "trialing"),
        ("active", "active"),
        ("past_due", "past_due"),
        ("canceled", "canceled"),
        ("unpaid", "unpaid"),
        (None, "None"),
    ]
    stripe_status = models.CharField(
        max_length=32, choices=STRIPE_STATUS_CHOICES, null=True, blank=True, default=None
    )

    #: Fin de periodo actual (para saber si aún está vigente)
    stripe_current_period_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        @brief Representación en texto del perfil.
        @return Cadena con el username del usuario.
        """
        return f'Perfil de {self.user.username}'

    # ---------------------------
    # Perfil: completitud de datos
    # ---------------------------
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

    # ---------------------------
    # Stripe: helpers
    # ---------------------------

    @property
    def has_active_subscription(self) -> bool:
        """
        @brief Indica si la suscripción se considera activa a nivel de negocio.
        @details
         Reglas comunes:
          - Estados 'trialing' y 'active' cuentan como activos.
          - 'past_due' puede considerarse activo durante el periodo vigente.
          - 'canceled' y 'unpaid' no son activos, salvo que el periodo no haya expirado (gracia).
        """
        now = timezone.now()
        status = (self.stripe_status or "").lower() if self.stripe_status else None

        if not status:
            return False

        if status in ("trialing", "active"):
            # Si Stripe dice activo/trial y la fecha de fin no expiró (o no está establecida), aceptamos
            return (self.stripe_current_period_end is None) or (self.stripe_current_period_end > now)

        if status == "past_due":
            # Permitimos acceso mientras no haya vencido el periodo actual
            return bool(self.stripe_current_period_end and self.stripe_current_period_end > now)

        if status in ("canceled", "unpaid", "incomplete", "incomplete_expired"):
            # Puede existir acceso por periodo pagado hasta su fin (gracia)
            return bool(self.stripe_current_period_end and self.stripe_current_period_end > now)

        return False

    def _stripe_configured(self) -> bool:
        """
        @brief Verifica que stripe esté disponible y configurado.
        """
        if stripe is None:
            print("[Stripe] Paquete 'stripe' no instalado (pip install stripe).")
            return False
        secret = getattr(settings, "STRIPE_SECRET_KEY", None)
        if not secret:
            print("[Stripe] STRIPE_SECRET_KEY no configurado en settings.")
            return False
        stripe.api_key = secret
        return True

    def ensure_stripe_customer(self) -> bool:
        """
        @brief Crea (si no existe) el Customer en Stripe y guarda el `stripe_customer_id`.
        @return True si hay Customer asegurado (ya existía o se creó), False si no fue posible.
        """
        if self.stripe_customer_id:
            return True
        if not self._stripe_configured():
            return False

        try:
            customer = stripe.Customer.create(
                email=self.user.email or None,
                name=f"{(self.user.first_name or '').strip()} {(self.user.last_name or '').strip()}".strip() or self.user.username,
                metadata={"django_user_id": str(self.user.id)}
            )
            self.stripe_customer_id = customer.get("id")
            self.save(update_fields=["stripe_customer_id"])
            return True
        except Exception as e:  # pragma: no cover
            print(f"[Stripe] Error creando Customer: {e}")
            return False

    def start_subscription(self, price_id: str, trial_days: int | None = None) -> bool:
        """
        @brief Inicia una suscripción en Stripe para el `price_id` indicado.
        @param price_id ID del precio (p.ej. 'price_ABC123')
        @param trial_days Días de prueba opcionales
        @return True si se inicia y sincroniza correctamente, False en caso contrario.
        @note Este método está pensado para flujos server-side sencillos (sin Checkout Session).
        """
        if not self.ensure_stripe_customer():
            return False
        if not self._stripe_configured():
            return False

        try:
            params = {
                "customer": self.stripe_customer_id,
                "items": [{"price": price_id}],
                "payment_behavior": "default_incomplete",
                "expand": ["latest_invoice.payment_intent"],
            }
            if trial_days and trial_days > 0:
                params["trial_period_days"] = trial_days

            subscription = stripe.Subscription.create(**params)

            # Guardar datos base y marcar para completar pago en frontend si aplica
            self.stripe_subscription_id = subscription.get("id")
            self.stripe_price_id = price_id
            self.stripe_status = subscription.get("status")
            period = subscription.get("current_period_end")
            self.stripe_current_period_end = timezone.datetime.fromtimestamp(period, tz=timezone.utc) if period else None
            self.is_subscribed = self.has_active_subscription
            self.save(update_fields=[
                "stripe_subscription_id", "stripe_price_id", "stripe_status",
                "stripe_current_period_end", "is_subscribed"
            ])
            return True
        except Exception as e:  # pragma: no cover
            print(f"[Stripe] Error iniciando suscripción: {e}")
            return False

    def sync_subscription(self) -> bool:
        """
        @brief Sincroniza campos locales con el estado real de Stripe.
        @return True si se sincronizó correctamente, False si no fue posible.
        """
        if not self._stripe_configured():
            return False
        if not self.stripe_subscription_id:
            # No hay suscripción conocida que sincronizar
            self.is_subscribed = False
            self.save(update_fields=["is_subscribed"])
            return False

        try:
            sub = stripe.Subscription.retrieve(self.stripe_subscription_id)
            self.stripe_status = sub.get("status")
            period = sub.get("current_period_end")
            self.stripe_current_period_end = timezone.datetime.fromtimestamp(period, tz=timezone.utc) if period else None
            self.is_subscribed = self.has_active_subscription
            self.save(update_fields=["stripe_status", "stripe_current_period_end", "is_subscribed"])
            return True
        except Exception as e:  # pragma: no cover
            print(f"[Stripe] Error sincronizando suscripción: {e}")
            return False

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
        perfil, _ = Perfil.objects.get_or_create(user=instance)
        # Intentar crear automáticamente el Customer en Stripe (opcional)
        try:
            perfil.ensure_stripe_customer()
        except Exception as e:  # pragma: no cover
            # No bloquear el alta del usuario si falla Stripe
            print(f"[Stripe] Aviso: no se pudo crear Customer en alta de usuario: {e}")

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
