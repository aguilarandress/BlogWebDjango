from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("registrar/", views.registrarNuevoUsuario, name="registrarNuevoUsuario"),
    path("iniciarSesion/", views.iniciarSesion, name="iniciarSesion"),
    path("cerrarSesion/", views.cerrarSesion, name="cerrarSesion"),
    path("crearPost/", views.crearPost, name="crearPost"),
    path("post/<int:id>/", views.detallesPost, name="detallesPost"),
    path("post/<int:id>/comentar/", views.agregarComentario, name="agregarComentario"),
    path("post/<int:id>/like/", views.likePost, name="likePost"),
    path("post/<int:id>/dislike/", views.dislikePost, name="dislikePost")
]