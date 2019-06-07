from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class BlogPost(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=125)
    contenido = models.TextField()
    numDislikes = models.IntegerField(default=0)
    numLikes = models.IntegerField(default=0)
    fechaDelPost = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.titulo


class ComentarioBlog(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fechaDelComentario = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.contenido
