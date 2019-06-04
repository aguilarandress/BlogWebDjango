from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .helpers import validarDatosDeRegistro, validarDatosInicioSesion
from .models import BlogPost

def index(request):
    """Carga la página index del blog

    Entradas:
        request: es un objeto de petición Http
    Precondiciones:
        No hay
    Salidas:
        Retorna una respuesta al usuario
    """
    if request.method == "POST":
        tituloPost = request.POST["titulo"]
        contenidoPosr = request.POST["contenidoPost"]
        return HttpResponseRedirect(reverse("blog:index"))
    else:
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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("blog:index"))
    else:
        if request.method == "POST":
            # Obtener datos del formulario
            usuario = {
                "nombre": request.POST["nombre"],
                "email": request.POST["email"],
                "contraseña": request.POST["contraseña"],
                "contraseña2": request.POST["contraseña2"]
            }

            # Validar datos del formulario
            if not validarDatosDeRegistro(usuario)["esValido"]:
                for mensaje in validarDatosDeRegistro(usuario)["mensajes"]:
                    messages.error(request, mensaje)
                return render(request, "blog/registrar.html", usuario)

            # Revisar si existe un usuario con el nombre
            if User.objects.filter(username=usuario["nombre"]).exists():
                messages.error(request, "El nombre de usuario ya existe")
                return render(request, "blog/registrar.html", usuario)

            # Revisar si existe un usuario con el nombre
            if User.objects.filter(email=usuario["email"]).exists():
                messages.error(request, "El correo utilizado ya existe")
                return render(request, "blog/registrar.html", usuario)

            # Registrar usuario
            usuarioNuevo = User.objects.create_user(
                usuario["nombre"], usuario["email"], usuario["contraseña"])
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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("blog:index"))
    else:
        if request.method == "POST":
            # Obtener datos del formulario
            usuario = {"nombre": request.POST["nombre"],
                       "contraseña": request.POST["contraseña"]}
            # Validar datos del formulario
            if not validarDatosInicioSesion(usuario)["esValido"]:
                for mensaje in validarDatosInicioSesion(usuario)["mensajes"]:
                    messages.error(request, mensaje)
                return render(request, "blog/iniciarSesion.html", usuario)
            # Autorizar al usuario
            usuario = authenticate(
                request, username=usuario["nombre"], password=usuario["contraseña"])
            if not usuario:
                messages.error(
                    request, "Nombre de usuario o contraseña incorrectos")
                return render(request, "blog/iniciarSesion.html")
            else:
                login(request, usuario)
                messages.success(request, "Ha iniciado sesión correctamente")
                return HttpResponseRedirect(reverse("blog:index"))
        else:
            return render(request, "blog/iniciarSesion.html")


def cerrarSesion(request):
    logout(request)
    messages.success(request, "Ha cerrado su sesión correctamente")
    return HttpResponseRedirect(reverse("blog:iniciarSesion"))


@login_required(login_url='/iniciarSesion/')
def crearPost(request):
    if request.method == "POST":
        titulo = request.POST["titulo"]
        contenido = request.POST["contenido"]
        form = BlogPost(titulo=titulo, contenido=contenido)
        form.save()
        return HttpResponseRedirect(reverse("blog:index"))
    else:
        context = {
            "titulo": "Escriba su post"
        }
        return render(request, "blog/crearPost.html", context)
