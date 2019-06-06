from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("registrar/", views.registrarNuevoUsuario, name="registrarNuevoUsuario"),
    path("iniciarSesion/", views.iniciarSesion, name="iniciarSesion"),
    path("cerrarSesion/", views.cerrarSesion, name="cerrarSesion"),
    path("crearPost/", views.crearPost, name="crearPost"),
    path("post/<int:id>/", views.detallesPost, name="detallesPost")
]