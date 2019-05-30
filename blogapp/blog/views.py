from django.shortcuts import render
from django.http import HttpResponse


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
# Create your views here.


def inicioSesion(request):
    """Carga la página iniciar sesion en el blog

        Entradas:
            request: Es un objeto que representa un request
        Precondiciones:
            No hay
        Salidas:
            Retorna una respuesta al usuario
        """
    context = {
        "titulo": "TEC Blog, inicio de sesión"
    }
    return render(request, "blog/inicioSesion.html", context)


def crearUsuario(request):
    """Carga la página crearUsuarios del blog

        Entradas:
            request: Es un objeto que representa un request
        Precondiciones:
            No hay
        Salidas:
            Retorna una respuesta al usuario
        """
    context = {
        "titulo": "TEC Blog, crear usuario"
    }
    return render(request, "blog/crearUsuario.html", context)