from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import IntegerField


# Create your models here.
class User(AbstractUser):
    image=models.ImageField(upload_to='foto_autores',null=True)
    
    email = models.EmailField(('email address'), unique=True)
    location=models.CharField(max_length=45, null=True, blank=True)
    biography = models.CharField(max_length=250, null=True, blank=True)
    facebook=models.CharField(max_length=250,null=True, blank=True)
    instagram=models.CharField(max_length=250, null=True, unique=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'
    
    def __str__(self):
        return self.email
    
    
class Follower(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Seguidor')   
      

class Article(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    title=models.CharField(max_length=100,verbose_name='Titulo')
    photo=models.ImageField(upload_to='foto_articulos',verbose_name='imagen')
    introduction=models.CharField(max_length=450, verbose_name='Introduccion')
    content=models.CharField(max_length=2500, verbose_name='Contenido')
    date=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    likes=models.IntegerField(verbose_name='Me gusta', default=0)
    dislikes=models.IntegerField(verbose_name='No me gusta',default=0)
    comments=models.IntegerField(verbose_name='Comentarios',default=0)
    edited=models.BooleanField(default=False,verbose_name='Editado')
    
    class Meta:
        verbose_name='Articulo'
        verbose_name_plural='Articulos'

    def __str__(self):
        return self.title


class Comment(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    article=models.ForeignKey(Article, on_delete=models.CASCADE,verbose_name='Articulo')
    date=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    comment=models.CharField(max_length=300, verbose_name='Comentario')
    likes=models.IntegerField(verbose_name='Me gusta', default=0)
    dislikes=models.IntegerField(verbose_name='No me gusta',default=0)
    edited=models.BooleanField(default=False,verbose_name='Editado')
    
    class Meta:
        verbose_name='Comentario'
        verbose_name_plural='Comentarios'
        ordering = ['-date']
    
    def __str__(self):
        return self.comment
       
    
class SubComment(models.Model):
    commentFather=models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Comentario Padre')
    author=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    article=models.ForeignKey(Article, on_delete=models.CASCADE,verbose_name='Articulo')
    subcomment=models.CharField(max_length=300, verbose_name='Sub Comentario')
    date=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')
    likes=models.IntegerField(verbose_name='Me gusta', default=0)
    dislikes=models.IntegerField(verbose_name='No me gusta',default=0)
    edited=models.BooleanField(default=False,verbose_name='Editado')
    
    class Meta:
        verbose_name='Sub Comentario'
        verbose_name_plural='Sub Comentarios'
        ordering = ['-date']
    
    def __str__(self):
        return self.subcomment
    
    
class ArticleLikes(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    value=models.IntegerField(default=0)
    
    class Meta:
        verbose_name='Articulos Like'
        verbose_name_plural='Articulos Likes'


class CommentLikes(models.Model):
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    value=models.IntegerField(default=0)
    
    class Meta:
        verbose_name='Comentario Like'
        verbose_name_plural='Comentarios Likes'
    

class SubcommentLikes(models.Model):
    subcomment=models.ForeignKey(SubComment,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    value=models.IntegerField(default=0)