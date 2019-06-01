from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


def index(request):
    """Carga la página index del blog

    Entradas:
        request: Es un objeto que representa un request
    Precondiciones:
        No hay
    Salidas:
        Retorna una respuesta al usuario
    """
    context = {
        "titulo": "TEC Blog, by Andrew & Andres"
    }
    return render(request, "blog/index.html", context)


def registrarNuevoUsuario(request):
    if request.method == "POST":
        nombreDeUsuario = request.POST["nombre"]
        email = request.POST["email"]
        contraseña = request.POST["contraseña"]
        usuarioNuevo = User.objects.create_user(nombreDeUsuario, email, contraseña)
        usuarioNuevo.save()
        return HttpResponseRedirect(reverse("blog:iniciarSesion"))
    else:
        return render(request, "blog/registrar.html")


def iniciarSesion(request):
    return render(request, "blog/iniciarSesion.html")