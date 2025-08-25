from django.shortcuts import render

# Create your views here.

def panel_vendedor(request):
    return render(request, 'panel_vendedor.html')

def nueva_publicacion(request):
    return render(request, 'nueva_publicacion.html')

def edicion_publicacion(request, id):
    return render(request, 'edicion_publicacion.html')

def historial_publicaciones(request):
    return render(request, 'historial_publicaciones.html')