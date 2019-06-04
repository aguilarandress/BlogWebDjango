from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path("", include('blog.urls')),
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("registrar/", views.registrarNuevoUsuario, name="registrarNuevoUsuario"),
    path("iniciarSesion/", views.iniciarSesion, name="iniciarSesion"),
    path("cerrarSesion/", views.cerrarSesion, name="cerrarSesion"),
    path("crearPost/", views.crearPost, name="crearPost")
]
