from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("registrar/", views.registrarNuevoUsuario, name="registrarNuevoUsuario"),
    path("iniciarSesion/", views.iniciarSesion, name="iniciarSesion")
]