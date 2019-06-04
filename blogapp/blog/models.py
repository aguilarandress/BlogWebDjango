from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class BlogPost(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=125)
    contenido = models.TextField()
    num_dislikes = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)
    fechaDelPost = models.DateTimeField(default=datetime.now, blank=True)
