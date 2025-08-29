from django.contrib import admin
from .models import Publicacion, FotoPublicacion

class FotoInline(admin.TabularInline):
    model = FotoPublicacion
    extra = 1

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "tipo_operacion", "precio", "estatus", "ciudad", "estado", "fecha_creacion")
    list_filter = ("tipo_operacion", "estatus", "ciudad", "estado", "tipo_financiamiento")
    search_fields = ("titulo", "descripcion", "calle", "colonia", "ciudad", "estado", "codigo_postal")
    inlines = [FotoInline]

@admin.register(FotoPublicacion)
class FotoPublicacionAdmin(admin.ModelAdmin):
    list_display = ("publicacion", "es_portada", "orden", "fecha_subida")
    list_filter = ("es_portada",)