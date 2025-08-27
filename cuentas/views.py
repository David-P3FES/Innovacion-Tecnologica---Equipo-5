from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import perfil_incompleto
from .forms import PerfilForm
from django.urls import reverse


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
            return redirect('home')  # redirige a la home (que está en principal)
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'core/cuenta/completar_perfil.html', {'form': form})


@login_required
def perfil_usuario_guardado(request):
    if perfil_incompleto(request.user):
        return redirect('completar_perfil')
    return render(request, 'core/comprador/perfil_usuario.html')


def cuenta_redirect(request):
    # Redirige a la URL del login real de allauth (/accounts/login/)
    return redirect(reverse('account_login'))
