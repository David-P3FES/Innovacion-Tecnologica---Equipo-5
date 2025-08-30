# publicaciones/templatetags/publicaciones_extras.py
from django import template
from publicaciones.models import Publicacion

register = template.Library()

@register.simple_tag(takes_context=True)
def publicaciones_count(context):
    """
    Regresa el número de publicaciones del usuario autenticado.
    Si no hay usuario autenticado, regresa 0.
    """
    request = context.get("request")
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return 0
    return Publicacion.objects.filter(usuario=user).count()

@register.filter
def currency_mx(value):
    """
    Formatea un número como MXN sin decimales: 1200000 -> $1,200,000
    No lanza excepción si no es numérico.
    """
    try:
        n = float(value)
    except Exception:
        return value
    # usa separadores de miles con coma
    return "${:,.0f}".format(n)

@register.filter
def tidy_banos(value):
    """
    '1.0' -> '1', pero conserva '.5' (e.g. '1.5')
    """
    s = str(value)
    if s.endswith(".0"):
        return s[:-2]
    return s
