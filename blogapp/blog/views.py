from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .helpers import validarDatosDeRegistro


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
        "titulo": "Últimos posts publicados"
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
        # Obtener datos del formulario
        usuario = {
            "nombre": request.POST["nombre"],
            "email": request.POST["email"],
            "contraseña": request.POST["contraseña"],
            "contraseña2": request.POST["contraseña2"]
        }
        # TODO: Validar datos del formulario
        if not validarDatosDeRegistro(usuario)["esValido"]:
            for mensaje in validarDatosDeRegistro(usuario)["mensajes"]:
                messages.error(request, mensaje)
            return render(request, "blog/registrar.html", usuario)
        usuarioNuevo = User.objects.create_user(usuario["nombre"], usuario["email"], usuario["contraseña"])
        usuarioNuevo.save()

        messages.success(request, "Usuario registrado")
        return HttpResponseRedirect(reverse("blog:iniciarSesion"))
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
            messages.success(request, "Ha iniciado sesión correctamente")
            return HttpResponseRedirect(reverse("blog:index"))
        else:
            return HttpResponseRedirect(reverse("blog:iniciarSesion"))
    else:
        return render(request, "blog/iniciarSesion.html")