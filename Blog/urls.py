from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('',Articulos.as_view(), name='articulos'),
    path('accounts/login/',InicioSesion.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('registrarme/',Registro.as_view(), name='registro'),
    path('mis-articulos/<int:pk>',MisArticulos.as_view(), name='mis_articulos'),
    path('nuevo-articulo/',NuevoArticulo.as_view(), name='nuevo_articulo'),
    path('editar-articulo/<int:pk>',EditarArticulo, name='editar_articulo'),
    path('eliminar-articulo/',EliminarArticulo.as_view(), name='eliminar_articulo'),
    path('<int:pk>/<str:title>/',DetalleArticulo.as_view(), name='detalle_articulo'),
    path('comentario/',Comentar.as_view(), name='nuevo_comentario'),
    path('editar-comentarios/',EditarComentarios.as_view(), name='editar_comentarios'),
    path('eliminar-comentarios/',EliminarComentarios.as_view(), name='eliminar_comentarios'),
    path('subcomentario/',SubComentar.as_view(), name='nuevo_subcomentario'),
    path('article-nuevo-like/',ArticleLike.as_view(), name='nuevo_like'),
    path('article-nuevo-dislike/',ArticleDislike.as_view(), name='nuevo_dislike'),
    path('comment-nuevo-like/<int:value>/<int:pk>/<str:title>/<int:pka>/',CommentLike, name='nuevo_likec'),
    path('comment-nuevo-dislike/<int:value>/<int:pk>/<str:title>/<int:pka>/',CommentDislike, name='nuevo_dislikec'),
]