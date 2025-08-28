from django.shortcuts import render, redirect
from .models import Propiedad
from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated:
        perfil = getattr(request.user, "perfil", None)  # ← OJO: 'perfil'
        if perfil and not perfil.is_complete():
            return redirect('cuentas:complete_profile')
    return render(request, 'principal/home.html')

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

