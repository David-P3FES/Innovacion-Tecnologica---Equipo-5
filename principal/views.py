"""
@file views.py
@brief Vistas de la aplicación `principal`.
@details Define la lógica de las vistas principales:
         - Home con verificación de perfil.
         - Resultados de búsqueda de propiedades.
         - Página de detalle de prioridad (placeholder).
"""

from django.shortcuts import render, redirect
from .models import Propiedad
from django.http import HttpResponse


def home(request):
    """
    @brief Vista de inicio de la aplicación principal.
    @details
     - Si el usuario está autenticado pero su perfil no está completo,
       se le redirige a la vista `cuentas:complete_profile`.
     - En caso contrario, se carga la plantilla `principal/home.html`.

    @param request Objeto HttpRequest con información de la petición.
    @return HttpResponse con la página de inicio o redirección.
    """
    if request.user.is_authenticated:
        perfil = getattr(request.user, "perfil", None)  # perfil relacionado al user
        if perfil and not perfil.is_complete():
            return redirect('cuentas:complete_profile')
    return render(request, 'principal/home.html')


def resultados_busqueda(request):
    """
    @brief Vista de resultados de búsqueda de propiedades.
    @details
     - Recupera el parámetro `q` desde la URL.
     - Filtra las propiedades por título (coincidencia parcial, insensible a mayúsculas).
     - Solo se muestran aquellas con estado "disponible".
     - Si no hay query, retorna lista vacía.

    @param request Objeto HttpRequest con información de la petición.
    @return HttpResponse con la plantilla `principal/resultados_busqueda.html`
            y el contexto que incluye propiedades y la query.
    """
    query = request.GET.get('q')
    propiedades = Propiedad.objects.filter(
        titulo__icontains=query,
        estado='disponible'
    ) if query else []
    return render(request, 'principal/resultados_busqueda.html', {
        'propiedades': propiedades,
        'query': query
    })


def detalle_prioridad(request):
    """
    @brief Vista de detalle de prioridad (placeholder).
    @details
     - Devuelve un HttpResponse simple de prueba.
     - Pendiente de implementación futura para mostrar detalle real.

    @param request Objeto HttpRequest.
    @return HttpResponse con un mensaje de placeholder.
    """
    return HttpResponse("Aquí se mostrarán los detalles de la prioridad")
