from django.shortcuts import render
from .models import Propiedad
from django.http import HttpResponse


def home(request):
    # Filtros desde GET
    direccion = request.GET.get('direccion')
    tipo_operacion = request.GET.get('tipo_operacion')

    propiedades = Propiedad.objects.all()

    if direccion:
        propiedades = propiedades.filter(direccion__icontains=direccion)
    if tipo_operacion:
        propiedades = propiedades.filter(tipo_operacion=tipo_operacion)

    return render(request, 'principal/home.html', {
        'propiedades': propiedades
    })


def resultados_busqueda(request):
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
    return HttpResponse("Aquí se mostrarán los detalles de la prioridad")