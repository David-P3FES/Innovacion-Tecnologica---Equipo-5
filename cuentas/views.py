from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CompleteProfileForm

@login_required
def complete_profile(request):
    """
    Muestra/guarda el formulario de completar perfil.
    Tras guardar con éxito, manda a 'principal:home'.
    """
    perfil = request.user.perfil  # gracias a related_name='perfil'

    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, user=request.user, instance=perfil)
        if form.is_valid():
            perfil = form.save()
            print("✅ Perfil guardado correctamente:", perfil.rfc, perfil.whatsapp)  # DEBUG
            return redirect('principal:home')  
        else:
            print("❌ Errores de validación:", form.errors)  # DEBUG
    else:
        form = CompleteProfileForm(user=request.user, instance=perfil)

    return render(request, 'cuentas/completar_perfil.html', {'form': form})


@login_required
def post_login(request):
    """
    Decide a dónde mandar tras iniciar sesión:
    - Si el perfil NO está completo -> completar perfil
    - Si está completo -> principal:home
    """
    perfil = getattr(request.user, 'perfil', None)
    if perfil and not perfil.is_complete():
        return redirect('cuentas:complete_profile')
    return redirect('principal:home')
