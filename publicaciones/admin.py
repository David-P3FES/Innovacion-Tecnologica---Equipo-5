from django.contrib import admin
from django.apps import apps
from .models import Publicacion, Favorito

Publicacion = apps.get_model("publicaciones", "Publicacion")
FotoPublicacion = apps.get_model("publicaciones", "FotoPublicacion")

def _field_names(model):
    return {f.name for f in model._meta.get_fields()}

_P_fields = _field_names(Publicacion)

class SafeAdmin(admin.ModelAdmin):
    """Admin que arma list_display, filtros y ordenamiento solo con campos existentes."""

    base_list_display = ("id",)
    candidate_list_display = (
        "titulo", "usuario", "tipo_operacion", "precio",
        "estatus", "ciudad", "estado", "fecha_creacion",
    )
    candidate_list_filter = ("tipo_operacion", "estatus", "ciudad", "estado", "tipo_financiamiento")

    def get_list_display(self, request):
        return self.base_list_display + tuple(f for f in self.candidate_list_display if f in _P_fields)

    def get_list_filter(self, request):
        return tuple(f for f in self.candidate_list_filter if f in _P_fields)

    def get_ordering(self, request):
        # Usa fecha_creacion si existe; si no, cae a -id
        return ("-fecha_creacion",) if "fecha_creacion" in _P_fields else ("-id",)

@admin.register(Publicacion)
class PublicacionAdmin(SafeAdmin):
    search_fields = (
        "titulo", "descripcion", "calle", "colonia", "ciudad", "estado", "codigo_postal",
        "usuario__username", "usuario__email",
    )
    # readonly solo si existen
    def get_readonly_fields(self, request, obj=None):
        ro = []
        if "fecha_creacion" in _P_fields: ro.append("fecha_creacion")
        if "fecha_actualizacion" in _P_fields: ro.append("fecha_actualizacion")
        return tuple(ro)

@admin.register(FotoPublicacion)
class FotoPublicacionAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        fields = _field_names(FotoPublicacion)
        base = ("id",)
        candidates = ("publicacion", "orden", "es_portada", "fecha_subida")
        return base + tuple(f for f in candidates if f in fields)

    def get_list_filter(self, request):
        fields = _field_names(FotoPublicacion)
        return tuple(f for f in ("es_portada",) if f in fields)

    def get_ordering(self, request):
        fields = _field_names(FotoPublicacion)
        if {"publicacion", "orden"} <= fields:
            return ("publicacion", "orden")
        return ("id",)

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "publicacion", "creado")
    list_filter = ("creado",)
    search_fields = ("usuario__username", "publicacion__titulo")