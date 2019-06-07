from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .helpers import validarDatosDeRegistro, validarDatosInicioSesion, truncarContenido
from .models import BlogPost, ComentarioBlog, Estadisticas


def index(request):
    """Carga la página index del blog

    Entradas:
        request: es un objeto de petición Http
    Precondiciones:
        No hay
    Salidas:
        Retorna una respuesta al usuario
    """
    # Obtener los 10 blog posts más recientes
    posts = BlogPost.objects.order_by("-fechaDelPost")[:10]
    truncarContenido(posts)
    context = {"posts": posts}
    return render(request, "blog/index.html", context)


def detallesPost(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    comentarios = ComentarioBlog.objects.filter(post=post)
    blog_estadisticas = Estadisticas.objects.get(post=id)
    blog_estadisticas.num_visitas += 1
    blog_estadisticas.save()
    context = {"post": post, "comentarios": comentarios}
    return render(request, "blog/detallesPost.html", context)


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
            usuario = {"nombre": request.POST["nombre"], "contraseña": request.POST["contraseña"]}
            # Validar datos del formulario
            if not validarDatosInicioSesion(usuario)["esValido"]:
                for mensaje in validarDatosInicioSesion(usuario)["mensajes"]:
                    messages.error(request, mensaje)
                return render(request, "blog/iniciarSesion.html", usuario)
            # Autorizar al usuario
            usuario = authenticate(request, username=usuario["nombre"], password=usuario["contraseña"])
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


@login_required(login_url='/iniciarSesion/')
def cerrarSesion(request):
    logout(request)
    messages.success(request, "Ha cerrado su sesión correctamente")
    return HttpResponseRedirect(reverse("blog:iniciarSesion"))


@login_required(login_url='/iniciarSesion/')
def crearPost(request):
    if request.method == "POST":
        usuario = request.user
        titulo = request.POST["titulo"]
        contenido = request.POST["contenido"]
        post = BlogPost(titulo=titulo, contenido=contenido, usuario=usuario)
        post.save()
        postId = BlogPost.objects.get(pk=post.id)
        blog_estadisticas = Estadisticas(post=postId)
        blog_estadisticas.save()
        messages.success(request, "Blog Post creado con éxito")
        return HttpResponseRedirect(reverse("blog:index"))
    else:
        return render(request, "blog/crearPost.html")


@login_required(login_url='/iniciarSesion/')
def agregarComentario(request, id):
    post = BlogPost.objects.get(id=id)
    usuario = request.user
    contenido = request.POST["texto"]
    if contenido != "":
        comentario = ComentarioBlog(contenido=contenido, usuario=usuario, post=post)
        comentario.save()
        blog_estadisticas = Estadisticas.objects.get(post=id)
        blog_estadisticas.num_comentarios += 1
        blog_estadisticas.save()
        messages.success(request, "Comentario creado con éxito")
    else:
        messages.error(request, "Comentario vacío")
    return HttpResponseRedirect(reverse("blog:detallesPost", args=[id]))



@login_required(login_url='/iniciarSesion/')
def likePost(request, id):

    post = BlogPost.objects.get(pk=id)
    post.numLikes += 1
    blog_estadisticas = Estadisticas.objects.get(post=id)
    blog_estadisticas.porcentajeLikes = (post.numLikes / blog_estadisticas.num_visitas) * 100
    blog_estadisticas.save()
    post.save()
    return HttpResponseRedirect(reverse("blog:detallesPost", args=[id]))


@login_required(login_url='/iniciarSesion/')
def dislikePost(request, id):
    post = BlogPost.objects.get(pk=id)
    post.numDislikes += 1
    post.save()
    return HttpResponseRedirect(reverse("blog:detallesPost", args=[id]))
