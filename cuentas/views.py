"""
@file views.py
@brief Vistas de la aplicación `cuentas`.
@details
 Contiene las vistas relacionadas con la gestión de perfiles de usuario:
  - Completar perfil
  - Redirección post-login
  - Visualización de perfil
  - Edición de perfil
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CompleteProfileForm


@login_required
def complete_profile(request):
    """
    @brief Muestra y procesa el formulario de completar perfil.
    @details
     - Si el método es POST: valida y guarda los datos en el perfil del usuario.
     - Tras guardar correctamente, redirige a `principal:home`.
     - Si hay errores, vuelve a mostrar el formulario con mensajes de error.
     - Si el método es GET: muestra el formulario con los datos actuales del perfil.
    @param request Objeto HttpRequest del usuario autenticado.
    @return HttpResponse con la plantilla `cuentas/completar_perfil.html`.
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
    @brief Decide a dónde redirigir tras iniciar sesión.
    @details
     - Si el perfil del usuario no está completo → redirige a `cuentas:complete_profile`.
     - Si el perfil está completo → redirige a `principal:home`.
    @param request Objeto HttpRequest del usuario autenticado.
    @return HttpResponseRedirect a la ruta correspondiente.
    """
    perfil = getattr(request.user, 'perfil', None)
    if perfil and not perfil.is_complete():
        return redirect('cuentas:complete_profile')
    return redirect('principal:home')


@login_required
def ver_perfil(request):
    """
    @brief Muestra los datos del perfil del usuario.
    @param request Objeto HttpRequest del usuario autenticado.
    @return HttpResponse con la plantilla `cuentas/ver_perfil.html`.
    """
    perfil = request.user.perfil
    return render(request, "cuentas/ver_perfil.html", {"perfil": perfil, "user": request.user})


@login_required
def editar_perfil(request):
    """
    @brief Permite editar el perfil del usuario autenticado.
    @details
     - Si el método es POST: procesa el formulario y guarda cambios en el perfil.
     - Si es válido, redirige a `cuentas:ver_perfil`.
     - Si es GET o el formulario tiene errores: muestra el formulario prellenado.
    @param request Objeto HttpRequest del usuario autenticado.
    @return HttpResponse con la plantilla `cuentas/editar_perfil.html`.
    """
    perfil = request.user.perfil

    if request.method == "POST":
        form = CompleteProfileForm(request.POST, user=request.user, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("cuentas:ver_perfil")
    else:
        form = CompleteProfileForm(user=request.user, instance=perfil)

    return render(request, "cuentas/editar_perfil.html", {"form": form})
