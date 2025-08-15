from django.shortcuts import render

# 1. Páginas públicas
def home(request):
    return render(request, 'core/public/home.html')

def resultados_busqueda(request):
    return render(request, 'core/public/resultados_busqueda.html')

def detalle_propiedad(request, id):
    return render(request, 'core/public/detalle_propiedad.html')

def registro_login(request):
    return render(request, 'core/public/registro_login.html')

def planes_precios(request):
    return render(request, 'core/public/planes_precios.html')

# 2. Privadas - Comprador/Rentador
def perfil_usuario(request):
    return render(request, 'core/comprador/perfil_usuario.html')

def lista_deseos(request):
    return render(request, 'core/comprador/lista_deseos.html')

# 3. Privadas - Vendedor
def panel_vendedor(request):
    return render(request, 'core/vendedor/panel_vendedor.html')

def nueva_publicacion(request):
    return render(request, 'core/vendedor/nueva_publicacion.html')

def edicion_publicacion(request, id):
    return render(request, 'core/vendedor/edicion_publicacion.html')

def historial_publicaciones(request):
    return render(request, 'core/vendedor/historial_publicaciones.html')

# 4. Privadas - Administrador
def panel_administracion(request):
    return render(request, 'core/admin/panel_administracion.html')

