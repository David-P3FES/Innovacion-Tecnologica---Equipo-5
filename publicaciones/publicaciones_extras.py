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
