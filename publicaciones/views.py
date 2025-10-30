# publicaciones/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import Publicacion
from .forms import PublicacionForm, FotoPublicacionFormSet
from django.db.models import Q, Count
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render


def _normalizar_portada(publicacion):
    fotos = list(publicacion.fotos.order_by("orden", "id"))
    if not fotos:
        return
    # contar marcadas
    marcadas = [f for f in fotos if f.es_portada]
    if len(marcadas) == 0:
        # ninguna portada → primera como portada
        fotos[0].es_portada = True
        fotos[0].save(update_fields=["es_portada"])
        # las demás a False por si habían quedado en True en otro estado
        for f in fotos[1:]:
            if f.es_portada:
                f.es_portada = False
                f.save(update_fields=["es_portada"])
    elif len(marcadas) > 1:
        # varias portadas → dejar solo la primera (por orden)
        primera = marcadas[0]
        for f in fotos:
            f.es_portada = (f.pk == primera.pk)
            f.save(update_fields=["es_portada"])
    # si ya había exactamente una, no hacemos nada


@login_required
def crear_publicacion(request):
    if request.method == "POST":
        form = PublicacionForm(request.POST, request.FILES)
        formset = FotoPublicacionFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.save()
            formset.instance = publicacion
            formset.save()
            _normalizar_portada(publicacion)
            messages.success(request, "¡Publicación creada correctamente!")
            # Antes: return redirect("publicaciones:editar", pk=publicacion.pk)
            return redirect("publicaciones:panel")  # ⬅️ redirige al panel
    else:
        form = PublicacionForm()
        formset = FotoPublicacionFormSet()

    return render(request, "publicaciones/publicacion_form.html", {
        "form": form,
        "formset": formset,
        "modo": "crear",
    })

@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        formset = FotoPublicacionFormSet(request.POST, request.FILES, instance=publicacion)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            _normalizar_portada(publicacion)
            messages.success(request, "¡Publicación actualizada!")
            # Antes: return redirect("publicaciones:editar", pk=publicacion.pk)
            return redirect("publicaciones:panel")   # ⬅️ ahora al panel
    else:
        form = PublicacionForm(instance=publicacion)
        formset = FotoPublicacionFormSet(instance=publicacion)

    return render(request, "publicaciones/publicacion_form.html", {
        "form": form,
        "formset": formset,
        "modo": "editar",
        "publicacion": publicacion,
    })

@login_required
def panel_ventas(request):
    """
    Lista sólo las publicaciones del usuario autenticado,
    ordenadas por fecha_creacion desc (definido en Meta).
    Incluye paginación y conteos por estatus.
    """
    base_qs = Publicacion.objects.filter(usuario=request.user)
    # ⬇️ Conteos por estatus
    stats = base_qs.aggregate(
        total=Count('id'),
        disponibles=Count('id', filter=Q(estatus='disponible')),
        en_trato=Count('id', filter=Q(estatus='en_trato')),
        cerradas=Count('id', filter=Q(estatus='cerrada')),
    )

    # filtros rápidos
    qs = base_qs
    estatus = request.GET.get("estatus")
    operacion = request.GET.get("operacion")
    if estatus:
        qs = qs.filter(estatus=estatus)
    if operacion:
        qs = qs.filter(tipo_operacion=operacion)

    paginator = Paginator(qs.prefetch_related("fotos"), 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "publicaciones/panel_ventas.html", {
        "page_obj": page_obj,
        "estatus_sel": estatus or "",
        "operacion_sel": operacion or "",
        "stats": stats, 
        "is_subscribed": getattr(request.user.perfil, "is_subscribed", False)
    })



@login_required
@require_POST
def cambiar_estatus(request, pk):
    """
    Cambia el estatus de una publicación del usuario.
    Acepta valores: disponible | en_trato | cerrada
    """
    publicacion = get_object_or_404(Publicacion, pk=pk, usuario=request.user)
    nuevo = request.POST.get("estatus")
    validos = {"disponible", "en_trato", "cerrada"}
    if nuevo not in validos:
        messages.error(request, "Estatus inválido.")
        return redirect("publicaciones:panel")

    publicacion.estatus = nuevo
    publicacion.save(update_fields=["estatus"])
    messages.success(request, "Estatus actualizado.")
    return redirect("publicaciones:panel")


@login_required
@require_POST
def eliminar_publicacion(request, pk):
    """
    Elimina una publicación del usuario (con confirmación por POST).
    """
    publicacion = get_object_or_404(Publicacion, pk=pk, usuario=request.user)
    titulo = publicacion.titulo
    publicacion.delete()
    messages.success(request, f"‘{titulo}’ eliminada correctamente.")
    return redirect("publicaciones:panel")