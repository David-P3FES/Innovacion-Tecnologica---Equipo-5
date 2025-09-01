from django.urls import path
from . import views

app_name = "publicaciones"

urlpatterns = [
    path("nueva/", views.crear_publicacion, name="crear"),
    path("<int:pk>/editar/", views.editar_publicacion, name="editar"),

    # Panel de ventas
    path("panel/", views.panel_ventas, name="panel"),
    path("<int:pk>/cambiar-estatus/", views.cambiar_estatus, name="cambiar_estatus"),
    path("<int:pk>/eliminar/", views.eliminar_publicacion, name="eliminar"),

]
