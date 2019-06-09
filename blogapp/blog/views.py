from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .helpers import validarDatosDeRegistro, validarContenido, truncarContenido
from .models import BlogPost, ComentarioBlog, Estadisticas


def index(request):
    """Carga la página index del blog

    Entradas:
        request: es un objeto de petición Http
    Precondiciones:
        No hay
    Salidas:
        Retorna un HttpResponse con el template respectivo
    Proceso:
        1. Se obtienen los 10 posts más recientes ordenados
        post la fecha más reciente
        2. Se trunca el contenido de los posts
        3. Se retorna el template con los posts
    """
    # Obtener los 10 blog posts más recientes
    posts = BlogPost.objects.order_by("-fechaDelPost")[:10]
    truncarContenido(posts)
    context = {"posts": posts}
    return render(request, "blog/index.html", context)


def detallesPost(request, id):
    """Carga la página de un post

    Entradas:
        request: es un objeto de petición Http
        id: es un id de un post
    Precondiciones:
        No hay
    Salidas:
        Retorna un render() con el template de 
        detallesPost
    Proceso:
        1. Obtiene el post con el id
        2. Obtiene los comentarios del post respectivo
        3. Se aumenta el número de visitas
        4. Se carga el post y los comentarios en el template
    """
    post = get_object_or_404(BlogPost, pk=id)
    comentarios = ComentarioBlog.objects.filter(post=post)
    # Actualizar estadísticas
    blogEstadisticas = Estadisticas.objects.get(post=id)
    blogEstadisticas.numVisitas += 1
    blogEstadisticas.save()
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
    Proceso:
        1. Se revisa si el usuario no ha iniciado sesión para 
        que continue con el proceso de registro
        2. Dependiendo del tipo de request, se carga el template
        o se carga procesa el formulario
        3. Con tres condicionales se valida la información del formulario,
        si el username ya fue utilizado o el correo
        4. Se crea el usuario y se guarda
        5. El usuario se redirige a iniciar sesión
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
        retorna un HttpResponseRedirect cuando un usuario inicia
        sesión con éxito
    Proceso:
        1. Se revisa si el usuario no ha iniciado sesión para 
        que continue con el proceso de registro
        2. Dependiendo del tipo de request, se carga el template
        o se carga procesa el formulario
        3. Se valida el contenido del formulario de inicio de sesión
        4. Con la función authenticate() y con condicional se autoriza
        al usuario hacer login
        5. Con la función login se inicia sesión y se redirige a la
        página de inicio
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("blog:index"))
    else:
        if request.method == "POST":
            # Obtener datos del formulario
            usuario = {"nombre": request.POST["nombre"], "contraseña": request.POST["contraseña"]}
            # Validar datos del formulario
            if not validarContenido(usuario)["esValido"]:
                for mensaje in validarContenido(usuario)["mensajes"]:
                    messages.error(request, mensaje)
                return render(request, "blog/iniciarSesion.html", usuario)

            # Autorizar al usuario
            usuario = authenticate(request, username=usuario["nombre"], password=usuario["contraseña"])
            if not usuario:
                messages.error(request, "Nombre de usuario o contraseña incorrectos")
                return render(request, "blog/iniciarSesion.html")
            else:
                login(request, usuario)
                messages.success(request, "Ha iniciado sesión correctamente")
                return HttpResponseRedirect(reverse("blog:index"))
        else:
            return render(request, "blog/iniciarSesion.html")


@login_required(login_url='/iniciarSesion/')
def cerrarSesion(request):
    """Cierra la sesión de un usuario

    Entradas:
        request: es un objeto de petición Http
    Precondiciones:
        No hay
    Salidas:
        Retorna un  HttpResponseRedirect
    Proceso:
        1. Con la función logout() se cierra la sesión
        del usuario
        2. Se redirige a la página de iniciar sesión
    """
    logout(request)
    messages.success(request, "Ha cerrado su sesión correctamente")
    return HttpResponseRedirect(reverse("blog:iniciarSesion"))


@login_required(login_url='/iniciarSesion/')
def crearPost(request):
    """Crea un nuevo post

    Entradas:
        request: es un objeto de petición Http
    Precondiciones:
        No hay
    Salidas:
        Retorna un template cuando se carga la interfaz y
        retorna un HttpResponseRedirect cuando un post se
        crea con éxito
    Proceso:
        1. Se revisa el tipo de petición
        2. Se valida el formulario para crear el post
        3. Se crea el post y sus estadísticas y finalmente
        se guarda
        4. Se envía el correo al usuario con send_mail()
        5. Se redirige al usuario a la página index
    """
    if request.method == "POST":
        post = {"titulo": request.POST["titulo"], "contenido": request.POST["contenido"]}
        # Validar datos del formulario
        if not validarContenido(post)["esValido"]:
            for mensaje in validarContenido(post)["mensajes"]:
                messages.error(request, mensaje)
            return render(request, "blog/crearPost.html", post)
        usuario = request.user
        # Crear y guardar post
        post = BlogPost(titulo=post["titulo"], contenido=post["contenido"], usuario=usuario)
        post.save()

        send_mail(
            "Blog creado",
            "Blog creado con el título " + post.titulo,
            "tp3.andres.andrew@gmail.com",
            [usuario.email],
            fail_silently=False,
        )
        # Crear estadísticas
        blog_estadisticas = Estadisticas(post=post)
        blog_estadisticas.save()
        messages.success(request, "Blog Post creado con éxito")
        return HttpResponseRedirect(reverse("blog:index"))
    else:
        return render(request, "blog/crearPost.html")


@login_required(login_url='/iniciarSesion/')
def agregarComentario(request, id):
    """Agrega un comentario al post

    Entradas:
        request: es un objeto de petición Http
        id: es un id de un post
    Precondiciones:
        No hay
    Salidas:
        Retorna un  HttpResponseRedirect
    Proceso:
        1. Se obtiene el post con el ID
        2. Se obtiene el usuario
        3. Se valida el comentario del blog
        4. El comentario es creado y guardado y las estadísticas
        se actualizan
        5. Se redirige a la página del post
    """
    post = BlogPost.objects.get(id=id)
    usuario = request.user
    contenido = request.POST["texto"]

    if contenido != "":
        comentario = ComentarioBlog(contenido=contenido, usuario=usuario, post=post)
        comentario.save()

        blogEstadisticas = Estadisticas.objects.get(post=id)
        blogEstadisticas.numComentarios += 1
        blogEstadisticas.save()

        messages.success(request, "Comentario creado con éxito")
    else:
        messages.error(request, "Comentario vacío")
    return HttpResponseRedirect(reverse("blog:detallesPost", args=[id]))


@login_required(login_url='/iniciarSesion/')
def likePost(request, id):
    """Le da like a un post

    Entradas:
        request: es un objeto de petición Http
        id: es un id de un post
    Precondiciones:
        No hay
    Salidas:
        Retorna un HttpResponseRedirect
    Proceso:
        1. Obtiene el post con el id
        2. Aumenta los likes
        3. Se obtienen las estadisticas del post
        4. Se guardan las estadísticas y el post
        5. Se redirige a la página de detalles
    """
    post = BlogPost.objects.get(pk=id)
    post.numLikes += 1
    blogEstadisticas = Estadisticas.objects.get(post=post)
    blogEstadisticas.porcentajeLikes = (post.numLikes * 100) / (post.numLikes + post.numDislikes)
    blogEstadisticas.save()
    post.save()
    return HttpResponseRedirect(reverse("blog:detallesPost", args=[id]))


@login_required(login_url='/iniciarSesion/')
def dislikePost(request, id):
    """Le da dislike a un post

    Entradas:
        request: es un objeto de petición Http
        id: es un id de un post
    Precondiciones:
        No hay
    Salidas:
        Retorna un HttpResponseRedirect
    Proceso:
        1. Obtiene el post con el id
        2. Aumenta los dislikes
        3. Se obtienen las estadisticas del post
        4. Se guardan las estadísticas y el post
        5. Se redirige a la página de detalles
    """
    post = BlogPost.objects.get(pk=id)
    post.numDislikes += 1
    blogEstadisticas = Estadisticas.objects.get(post=post)
    blogEstadisticas.porcentajeLikes = (post.numLikes * 100) / (post.numLikes + post.numDislikes)
    blogEstadisticas.save()
    post.save()
    return HttpResponseRedirect(reverse("blog:detallesPost", args=[id]))


@login_required(login_url='/iniciarSesion/')
def cuenta(request):
    """Carga la cuenta del usuario

    Entradas:
        request: es un objeto de petición Http
    Precondiciones:
        No hay
    Salidas:
        Retorna un template cuando se carga la interfaz
    Proceso:
        1. Se obtienen los posts del usuario
        2. Se itera sobre cada post y se obtienen sus
        estadísticas y se guardan en una lista
        3. Se carga el template con las estadísticas
    """
    usuario = request.user
    postsDelUsuario = BlogPost.objects.filter(usuario=usuario)

    estadisticasPosts = []
    for post in postsDelUsuario:
        estadisticas = Estadisticas.objects.get(post=post)
        estadisticasPosts.append(estadisticas)

    context = {"estadisticasPosts": estadisticasPosts}
    return render(request, "blog/cuenta.html", context)

