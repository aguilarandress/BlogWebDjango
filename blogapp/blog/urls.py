from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("inicioSesion/crearUsuario/", views.crearUsuario,  name="crearUsuario"),
    path("inicioSesion/", views.inicioSesion,  name="inicioSesion"),


]