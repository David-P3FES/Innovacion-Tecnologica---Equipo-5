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


def _to_decimal(s):
    try:
        return float(str(s).replace(",", "").strip())
    except Exception:
        return None

def resultados_busqueda(request):
    """
    Resultados de búsqueda pública con panel de filtros.
    Parámetros GET soportados:
      - direccion (texto libre: calle/colonia/ciudad/estado/CP/título/descr)
      - tipo_operacion: venta|renta
      - precio_min, precio_max (números)
      - rec_min, banos_min, est_min (números)
      - m2c_min, m2t_min (números)
      - financiamiento: contado|credito|ambos
      - estado, ciudad (texto)
    """
    # ── 1) Leer parámetros
    texto = (request.GET.get("direccion") or "").strip()
    tipo_sel = (request.GET.get("tipo_operacion") or "").strip().lower()
    financiamiento = (request.GET.get("financiamiento") or "").strip().lower()
    estado = (request.GET.get("estado") or "").strip()
    ciudad = (request.GET.get("ciudad") or "").strip()

    precio_min = _to_decimal(request.GET.get("precio_min"))
    precio_max = _to_decimal(request.GET.get("precio_max"))
    rec_min    = _to_decimal(request.GET.get("rec_min"))
    banos_min  = _to_decimal(request.GET.get("banos_min"))
    est_min    = _to_decimal(request.GET.get("est_min"))
    m2c_min    = _to_decimal(request.GET.get("m2c_min"))  # construcción
    m2t_min    = _to_decimal(request.GET.get("m2t_min"))  # terreno

    # ── 2) Base queryset (solo disponibles)
    qs = Publicacion.objects.filter(estatus="disponible")

    # ── 3) Filtros exactos / choices
    if tipo_sel in ("venta", "renta"):
        qs = qs.filter(tipo_operacion=tipo_sel)
    if financiamiento in ("contado", "credito", "ambos"):
        qs = qs.filter(tipo_financiamiento=financiamiento)

    # ── 4) Filtros numéricos
    if precio_min is not None:
        qs = qs.filter(precio__gte=precio_min)
    if precio_max is not None:
        qs = qs.filter(precio__lte=precio_max)

    if rec_min is not None:
        qs = qs.filter(recamaras__gte=int(rec_min))
    if banos_min is not None:
        qs = qs.filter(banos__gte=banos_min)
    if est_min is not None:
        qs = qs.filter(estacionamientos__gte=int(est_min))

    if m2c_min is not None:
        qs = qs.filter(metros_construccion__gte=int(m2c_min))
    if m2t_min is not None:
        qs = qs.filter(metros_terreno__gte=int(m2t_min))

    # ── 5) Ubicación
    if estado:
        qs = qs.filter(estado__icontains=estado)
    if ciudad:
        qs = qs.filter(ciudad__icontains=ciudad)

    # ── 6) Búsqueda por texto (tokenizada)
    if texto:
        tokens = [t for t in texto.replace(",", " ").split() if len(t) >= 2]
        campos = [
            "titulo__icontains",
            "descripcion__icontains",
            "calle__icontains",
            "numero__icontains",
            "colonia__icontains",
            "ciudad__icontains",
            "estado__icontains",
            "codigo_postal__icontains",
        ]
        for tk in tokens:
            or_block = Q()
            for c in campos:
                or_block |= Q(**{c: tk})
            qs = qs.filter(or_block)

    # ── 7) Optimización y orden
    qs = qs.select_related("usuario__perfil").prefetch_related("fotos").order_by("-fecha_creacion")

    # ── 8) Paginación
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    ctx = {
        "page_obj": page_obj,
        "total": paginator.count,
        "tipo_sel": tipo_sel,
        "q": texto,

        # Para mantener estado del formulario en la plantilla
        "precio_min": request.GET.get("precio_min", ""),
        "precio_max": request.GET.get("precio_max", ""),
        "rec_min": request.GET.get("rec_min", ""),
        "banos_min": request.GET.get("banos_min", ""),
        "est_min": request.GET.get("est_min", ""),
        "m2c_min": request.GET.get("m2c_min", ""),
        "m2t_min": request.GET.get("m2t_min", ""),
        "financiamiento": financiamiento,
        "estado": estado,
        "ciudad": ciudad,
    }
    return render(request, "principal/resultados_busqueda.html", ctx)


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
