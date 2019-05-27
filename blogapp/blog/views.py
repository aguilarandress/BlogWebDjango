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
