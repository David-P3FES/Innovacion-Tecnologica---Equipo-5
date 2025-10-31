from django.shortcuts import redirect
from django.urls import reverse

class RequireCompleteProfileMiddleware:
    """
    Si el usuario está autenticado y su perfil está incompleto, lo redirige a
    `cuentas:complete_profile` en cualquier URL que no esté en la lista blanca.
    Deja pasar logout, login, signup, static/media/admin.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self._computed = False
        self.exempt_paths = set()
        self.exempt_prefixes = ("/static/", "/media/", "/admin/")

    def _compute_exempt(self):
        names = [
            "cuentas:complete_profile",
            "cuentas:post_login",
            "account_login",
            "account_logout",
            "account_signup",
            "socialaccount_signup",
            "account_email_verification_sent",
            "account_confirm_email",
            "account_reset_password",
            "account_reset_password_done",
            "account_reset_password_from_key",
            "account_reset_password_from_key_done",
        ]
        for n in names:
            try:
                self.exempt_paths.add(reverse(n))
            except Exception:
                pass
        self._computed = True

    def __call__(self, request):
        if not self._computed:
            self._compute_exempt()

        path = request.path

        if path.startswith(self.exempt_prefixes):
            return self.get_response(request)

        user = request.user
        if not user.is_authenticated:
            return self.get_response(request)

        if path in self.exempt_paths:
            return self.get_response(request)

        try:
            complete_profile_path = reverse("cuentas:complete_profile")
        except Exception:
            complete_profile_path = "/cuentas/completar/"
        if path == complete_profile_path:
            return self.get_response(request)

        perfil = getattr(user, "perfil", None)
        is_incomplete = bool(perfil is not None and hasattr(perfil, "is_complete") and not perfil.is_complete())

        if is_incomplete:
            return redirect("cuentas:complete_profile")

        return self.get_response(request)
