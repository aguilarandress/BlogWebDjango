from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError


def index(request):
    """Carga la página index del blog

    Entradas:
        request: es un objeto de petición Http
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
    """Registra un usuario nuevo

    Entradas:
        request: es un objeto de petición Http
    Precondiciones:
        No hay
    Salidas:
        Retorna un template cuando se carga la interfaz y
        retorna un HttpResponseRedirect cuando un usuario se
        registra con éxito
    """
    if request.method == "POST":
        nombreDeUsuario = request.POST["nombre"]
        email = request.POST["email"]
        contraseña = request.POST["contraseña"]
        usuario = authenticate(request, username=nombreDeUsuario, password=contraseña)
        if usuario is not None:
            return HttpResponseRedirect(reverse("blog:registrarNuevoUsuario"))
        else:
            try:
                usuarioNuevo = User.objects.create_user(nombreDeUsuario, email, contraseña)
                usuarioNuevo.save()
                return HttpResponseRedirect(reverse("blog:iniciarSesion"))
            except IntegrityError:
                return HttpResponseRedirect(reverse("blog:registrarNuevoUsuario"))
    else:
        return render(request, "blog/registrar.html")


def iniciarSesion(request):
    """Registra un usuario nuevo

    Entradas:
        request: es un objeto de petición Http
    Precondiciones:
        No hay
    Salidas:
        Retorna un template cuando se carga la interfaz y
        retorna un HttpResponseRedirect cuando un usuario se
        registra con éxito
    """
    if request.method == "POST":
        nombreDeUsuario = request.POST["nombre"]
        contraseña = request.POST["contraseña"]
        usuario = authenticate(request, username=nombreDeUsuario, password=contraseña)
        if usuario is not None:
            login(request, usuario)
            return HttpResponseRedirect(reverse("blog:index"))
        else:
            return HttpResponseRedirect(reverse("blog:iniciarSesion"))
    else:
        return render(request, "blog/iniciarSesion.html")

