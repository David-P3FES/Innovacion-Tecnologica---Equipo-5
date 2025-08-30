# publicaciones/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# ──────────────────────────────────────────────────────────────────────────────
# Choices reutilizables (evita strings "mágicos")
# ──────────────────────────────────────────────────────────────────────────────
TIPO_OPERACION = (
    ("venta", "Venta"),
    ("renta", "Renta"),
)

TIPO_FINANCIAMIENTO = (
    ("contado", "Contado"),
    ("credito", "Crédito"),
    ("ambos", "Crédito o contado"),
)

ESTATUS_PUBLICACION = (
    ("disponible", "Disponible"),
    ("en_trato", "En trato"),
    ("cerrada", "Vendida/Rentada"),
)

# Validador de CP (México): 5 dígitos
cp_validator = RegexValidator(
    regex=r"^\d{5}$",
    message="El código postal debe tener exactamente 5 dígitos."
)

class Publicacion(models.Model):
    """
    Una Publicación representa una casa que un usuario sube para venta o renta.
    Campos principales: usuario, título, descripción, precio, tipo de operación.
    Incluye características, financiamiento, dirección (con lat/lon), estatus y timestamps.
    """
    # ─────────── Relación con el usuario propietario ───────────
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="publicaciones"
    )

    # ─────────── Identificación y detalle ───────────
    titulo = models.CharField(max_length=160)
    descripcion = models.TextField(blank=True)

    # ─────────── Económico ───────────
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    tipo_operacion = models.CharField(max_length=10, choices=TIPO_OPERACION)

    # ─────────── Características de la casa ───────────
    recamaras = models.PositiveIntegerField(default=0)
    banos = models.DecimalField(  # permite 1.5, 2.5, etc.
        max_digits=3, decimal_places=1, default=0,
        validators=[MinValueValidator(0)]
    )
    estacionamientos = models.PositiveIntegerField(default=0)
    metros_construccion = models.PositiveIntegerField(default=0)
    metros_terreno = models.PositiveIntegerField(default=0)

    # ─────────── Financiamiento ───────────
    tipo_financiamiento = models.CharField(max_length=12, choices=TIPO_FINANCIAMIENTO, default="ambos")

    # ─────────── Dirección ───────────
    calle = models.CharField(max_length=120)
    numero = models.CharField(max_length=20, blank=True)  # opcional (interior, s/n, etc.)
    colonia = models.CharField(max_length=120)
    ciudad = models.CharField(max_length=120)
    estado = models.CharField(max_length=120)
    codigo_postal = models.CharField(max_length=5, validators=[cp_validator])

    # ─────────── Coordenadas para mapa ───────────
    latitud = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )
    longitud = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )

    # ─────────── Estatus de la publicación ───────────
    estatus = models.CharField(max_length=12, choices=ESTATUS_PUBLICACION, default="disponible")

    # ─────────── Control de fechas ───────────
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-fecha_creacion",)
        indexes = [
            models.Index(fields=["estatus"]),
            models.Index(fields=["tipo_operacion"]),
            models.Index(fields=["ciudad", "estado"]),
            models.Index(fields=["precio"]),
        ]

    def __str__(self):
        return f"{self.titulo} · {self.get_tipo_operacion_display()} · ${self.precio}"

    # Helper para mostrar dirección completa en admin/plantillas
    @property
    def direccion_completa(self) -> str:
        num = f" #{self.numero}" if self.numero else ""
        return f"{self.calle}{num}, {self.colonia}, {self.ciudad}, {self.estado}, CP {self.codigo_postal}"

    # Indicador rápido para saber si tiene coordenadas válidas
    @property
    def tiene_coordenadas(self) -> bool:
        return self.latitud is not None and self.longitud is not None
    
    # al final de la clase Publicacion

    @property
    def foto_portada(self):
        """Devuelve la foto de portada (o la primera por orden) o None."""
        f = self.fotos.filter(es_portada=True).order_by("orden", "id").first()
        if not f:
            f = self.fotos.order_by("orden", "id").first()
        return f
    


class FotoPublicacion(models.Model):
    """
    Fotos asociadas a una Publicación (1:N).
    """
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name="fotos"
    )
    imagen = models.ImageField(upload_to="publicaciones/%Y/%m/%d/")
    # Campo opcional por si quieres destacar una foto en listados
    es_portada = models.BooleanField(default=False)
    # Orden opcional de aparición
    orden = models.PositiveIntegerField(default=0)

    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("orden", "id")
        indexes = [
            models.Index(fields=["publicacion", "orden"]),
        ]

    def __str__(self):
        return f"Foto #{self.pk} de {self.publicacion.titulo}"
