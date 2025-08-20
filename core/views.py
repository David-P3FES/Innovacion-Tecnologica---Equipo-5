from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Propiedad, perfil_incompleto  
from .forms import PerfilForm


def home(request):
    # Filtros desde GET
    direccion = request.GET.get('direccion')
    tipo_operacion = request.GET.get('tipo_operacion')

    propiedades = Propiedad.objects.all()

    if direccion:
        propiedades = propiedades.filter(direccion__icontains=direccion)
    if tipo_operacion:
        propiedades = propiedades.filter(tipo_operacion=tipo_operacion)

    return render(request, 'core/public/home.html', {
        'propiedades': propiedades
    })

def resultados_busqueda(request):
    query = request.GET.get('q')
    propiedades = Propiedad.objects.filter(titulo__icontains=query, estado='disponible') if query else []
    return render(request, 'core/public/resultados_busqueda.html', {'propiedades': propiedades, 'query': query})

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

@login_required
def completar_perfil(request):
    # Asegura que exista el perfil (por si el signal no se ejecutó aún)
    perfil = getattr(request.user, 'perfil', None)
    if perfil is None:
        from .models import Perfil
        perfil = Perfil.objects.create(user=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil se completó correctamente.')
            return redirect('home')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'core/cuenta/completar_perfil.html', {'form': form})


# Si quieres forzar perfil completo antes de entrar a secciones privadas:
# (Opcional: úsalo cuando gustes, no afecta lo que ya tienes)
@login_required
def perfil_usuario_guardado(request):
    if perfil_incompleto(request.user):
        return redirect('completar_perfil')
    return render(request, 'core/comprador/perfil_usuario.html')

