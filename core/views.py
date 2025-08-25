from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Propiedad
from django.shortcuts import redirect
from django.urls import reverse


def home(request):
    # Filtros desde GET
    direccion = request.GET.get('direccion')
    tipo_operacion = request.GET.get('tipo_operacion')

    propiedades = Propiedad.objects.all()

    if direccion:
        propiedades = propiedades.filter(direccion__icontains=direccion)
    if tipo_operacion:
        propiedades = propiedades.filter(tipo_operacion=tipo_operacion)

    return render(request, 'home.html', {
        'propiedades': propiedades
    })

def resultados_busqueda(request):
    query = request.GET.get('q')
    propiedades = Propiedad.objects.filter(titulo__icontains=query, estado='disponible') if query else []
    return render(request, 'resultados_busqueda.html', {'propiedades': propiedades, 'query': query})

def detalle_propiedad(request, id):
    return render(request, 'detalle_propiedad.html')



def planes_precios(request):
    return render(request, 'planes_precios.html')



def lista_deseos(request):
    return render(request, 'lista_deseos.html')
