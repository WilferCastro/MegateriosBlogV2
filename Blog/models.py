from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import IntegerField


# Create your models here.
class User(AbstractUser):
    image=models.ImageField(upload_to='foto_autores',null=True)
    
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'
    
    def __str__(self):
        return self.email
    
    

class Article(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    title=models.CharField(max_length=100,verbose_name='Titulo')
    photo=models.ImageField(upload_to='foto_articulos',verbose_name='imagen')
    introduction=models.CharField(max_length=100, verbose_name='Introduccion')
    date=models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    likes=models.IntegerField(verbose_name='Me gusta')
    dislikes=models.IntegerField(verbose_name='No me gusta')
    comments=models.IntegerField(verbose_name='Comentarios')
    
    class Meta:
        verbose_name='Articulo'
        verbose_name_plural='Articulos'

    def __str__(self):
        return self.title


class Comment(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    article=models.ForeignKey(Article, on_delete=models.CASCADE,verbose_name='Articulo')
    comment=models.CharField(max_length=200, verbose_name='Comentario')
    
    class Meta:
        verbose_name='Comentario'
        verbose_name_plural='Comentarios'
    
    def __str__(self):
        return self.comment