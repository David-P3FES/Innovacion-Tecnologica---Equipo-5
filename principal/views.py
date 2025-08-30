# principal/views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

# 👇 Importa el modelo real de tus listados (el que usas en el panel)
from publicaciones.models import Publicacion


def home(request):
    """
    Home con hero + buscador y 'Recientemente publicadas'.
    Trae solo publicaciones 'disponible', ordenadas por fecha (6).
    """
    recientes = (
        Publicacion.objects
        .filter(estatus="disponible")
        .select_related("usuario__perfil")        # ⚡ optimización
        .prefetch_related("fotos")                # ⚡ optimización
        .order_by("-fecha_creacion")[:6]
    )
    return render(request, "principal/home.html", {"recientes": recientes})


def resultados_busqueda(request):
    """
    Resultados de búsqueda pública:
    - Filtra por tipo_operacion (venta/renta) y por texto libre en dirección/título/etc.
    - Solo muestra 'disponible' (cara pública).
    """
    tipo = (request.GET.get('tipo_operacion') or '').strip().lower()
    texto = (request.GET.get('direccion') or '').strip()

    qs = Publicacion.objects.filter(estatus='disponible')

    if tipo in ('venta', 'renta'):
        qs = qs.filter(tipo_operacion=tipo)

    tokens = [t for t in texto.replace(',', ' ').split() if len(t) >= 2]
    campos = [
        'titulo__icontains',
        'descripcion__icontains',
        'calle__icontains',
        'numero__icontains',
        'colonia__icontains',
        'ciudad__icontains',
        'estado__icontains',
        'codigo_postal__icontains',
    ]
    for tk in tokens:
        or_block = Q()
        for c in campos:
            or_block |= Q(**{c: tk})
        qs = qs.filter(or_block)

    # ⚡ optimización: usuario/perfil + fotos en un solo query
    qs = qs.select_related("usuario__perfil").prefetch_related("fotos").order_by("-fecha_creacion")

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    ctx = {
        'page_obj': page_obj,
        'total': paginator.count,
        'tipo_sel': tipo,
        'q': texto,
    }
    return render(request, 'principal/resultados_busqueda.html', ctx)


# (Opcional) Si quieres actualizar "recientes" vía fetch sin recargar la página:
def recientes_html(request):
    recientes = (
        Publicacion.objects
        .filter(estatus="disponible")
        .select_related("usuario__perfil")        # ⚡ optimización
        .prefetch_related("fotos")                # ⚡ optimización
        .order_by("-fecha_creacion")[:6]
    )
    return render(request, "principal/_recientes.html", {"recientes": recientes})
