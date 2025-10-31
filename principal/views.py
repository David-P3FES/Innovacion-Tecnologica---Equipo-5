from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import unicodedata
from cuentas.models import perfil_incompleto


from publicaciones.models import Publicacion, Favorito, FotoPublicacion

def _to_decimal(s):
    """
    @brief Convierte string a decimal de forma segura
    @param s String a convertir
    @return Valor decimal o None si no es válido
    """
    try:
        return float(str(s).replace(",", "").strip())
    except Exception:
        return None

def _liked_ids_for(user, pubs_queryset_or_list):
    """
    @brief Obtiene IDs de publicaciones marcadas como favorito por el usuario
    @param user Usuario autenticado
    @param pubs_queryset_or_list Queryset o lista de publicaciones
    @return Set con IDs de publicaciones favoritas del usuario
    """
    if not user.is_authenticated:
        return set()
    ids = list(getattr(pubs_queryset_or_list, "values_list", lambda *a, **k: pubs_queryset_or_list)("id", flat=True))
    if not ids:
        return set()
    liked = Favorito.objects.filter(usuario=user, publicacion_id__in=ids).values_list("publicacion_id", flat=True)
    return set(liked)

def _quitar_acentos(texto):
    """
    @brief Normaliza texto removiendo acentos y caracteres especiales
    @param texto Texto a normalizar
    @return Texto normalizado en minúsculas sin acentos
    """
    if not texto:
        return ""
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(char for char in texto if unicodedata.category(char) != 'Mn')
    return texto.lower()

@login_required
def home(request):
    """
    @brief Vista principal con hero, buscador y publicaciones recientes
    @details Muestra las 6 publicaciones más recientes con estatus 'disponible'
    @param request Objeto HttpRequest
    @return HttpResponse renderizado con template home.html
    """
    recientes = (
        Publicacion.objects
        .filter(estatus="disponible")
        .select_related("usuario__perfil")
        .prefetch_related("fotos")
        .annotate(like_count=Count("favoritos"))
        .order_by("-fecha_creacion")[:6]
    )
    liked_ids = _liked_ids_for(request.user, recientes)

    return render(request, "principal/home.html", {
        "recientes": recientes,
        "liked_ids": liked_ids,
    })

def resultados_busqueda(request):
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
    m2c_min    = _to_decimal(request.GET.get("m2c_min"))
    m2t_min    = _to_decimal(request.GET.get("m2t_min"))

    qs = Publicacion.objects.filter(estatus="disponible")

    if tipo_sel in ("venta", "renta"):
        qs = qs.filter(tipo_operacion=tipo_sel)
    if financiamiento in ("contado", "credito", "ambos"):
        qs = qs.filter(tipo_financiamiento=financiamiento)

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

    if estado:
        qs = qs.filter(estado__icontains=estado)
    if ciudad:
        qs = qs.filter(ciudad__icontains=ciudad)

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
        
        qs_filtrado = qs
        for tk in tokens:
            or_block = Q()
            for c in campos:
                or_block |= Q(**{c: tk})
            qs_filtrado = qs_filtrado.filter(or_block)
        
        if not qs_filtrado.exists():
            texto_sin_acentos = _quitar_acentos(texto)
            ids_coincidentes = []
            
            for pub in qs:
                campos_texto = [
                    pub.titulo or "",
                    pub.descripcion or "",
                    pub.calle or "",
                    pub.numero or "",
                    pub.colonia or "",
                    pub.ciudad or "",
                    pub.estado or "",
                    pub.codigo_postal or "",
                ]
                
                texto_completo = " ".join(campos_texto).lower()
                texto_completo_sin_acentos = _quitar_acentos(texto_completo)
                
                if texto_sin_acentos in texto_completo_sin_acentos:
                    ids_coincidentes.append(pub.id)
            
            qs = qs.filter(id__in=ids_coincidentes)
        else:
            qs = qs_filtrado

    qs = (
        qs.select_related("usuario__perfil")
          .prefetch_related("fotos")
          .annotate(like_count=Count("favoritos"))
          .order_by("-fecha_creacion")
    )

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    liked_ids = _liked_ids_for(request.user, page_obj.object_list)

    ctx = {
        "page_obj": page_obj,
        "total": paginator.count,
        "tipo_sel": tipo_sel,
        "q": texto,


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
        "liked_ids": liked_ids,
    }
    return render(request, "principal/resultados_busqueda.html", ctx)

def recientes_html(request):
    """
    @brief Vista parcial para cargar publicaciones recientes via AJAX
    @param request Objeto HttpRequest
    @return HttpResponse con template parcial _recientes.html
    """
    recientes = (
        Publicacion.objects
        .filter(estatus="disponible")
        .select_related("usuario__perfil")
        .prefetch_related("fotos")
        .annotate(like_count=Count("favoritos"))
        .order_by("-fecha_creacion")[:6]
    )
    liked_ids = _liked_ids_for(request.user, recientes)
    return render(request, "principal/_recientes.html", {
        "recientes": recientes,
        "liked_ids": liked_ids,
    })

@login_required
def toggle_favorito(request, pk):
    """
    @brief Alterna el estado de favorito de una publicación via AJAX
    @param request Objeto HttpRequest (debe ser POST)
    @param pk ID de la publicación
    @return JsonResponse con estado {'liked': True|False}
    """
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    pub = get_object_or_404(Publicacion, pk=pk)
    obj, created = Favorito.objects.get_or_create(usuario=request.user, publicacion=pub)
    if not created:
        obj.delete()
    return JsonResponse({"liked": created})

@login_required
def mis_favoritos(request):
    """
    @brief Vista de listado de publicaciones favoritas del usuario
    @param request Objeto HttpRequest (requiere autenticación)
    @return HttpResponse con template mis_favoritos.html
    """
    pubs = (
        Publicacion.objects
        .filter(favoritos__usuario=request.user)
        .select_related("usuario__perfil")
        .prefetch_related("fotos")
        .annotate(like_count=Count("favoritos"))
        .order_by("-fecha_creacion")
    )
    liked_ids = _liked_ids_for(request.user, pubs)
    return render(request, "principal/mis_favoritos.html", {
        "publicaciones": pubs,
        "liked_ids": liked_ids,
    })


def publicacion_detalle(request, pk: int):
    """
    @brief Vista de detalle completo de una publicación
    @details Muestra información completa, galería de fotos, mapa y estado de favorito
    @param request Objeto HttpRequest
    @param pk ID de la publicación a mostrar
    @return HttpResponse con template publicacion_detalle.html
    """
    pub = (
        Publicacion.objects
        .select_related("usuario__perfil")
        .prefetch_related(
            Prefetch("fotos", queryset=FotoPublicacion.objects.order_by("orden", "id"))
        )
        .annotate(like_count=Count("favoritos"))
        .filter(pk=pk)
        .first()
    )
    if not pub:
        pub = get_object_or_404(Publicacion, pk=pk)

    liked = False
    if request.user.is_authenticated:
        liked = Favorito.objects.filter(usuario=request.user, publicacion=pub).exists()

    return render(request, "principal/publicacion_detalle.html", {
        "pub": pub,
        "liked": liked,
    })