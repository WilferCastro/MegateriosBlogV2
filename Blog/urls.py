from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('',Articulos, name='articulos'),
    path('accounts/login/',InicioSesion.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('registrarme/',Registro.as_view(), name='registro'),
    path('mis-articulos/<int:pk>',MisArticulos, name='mis_articulos'),
    path('nuevo-articulo/',NuevoArticulo.as_view(), name='nuevo_articulo'),
    path('editar-articulo/<int:pk>',EditarArticulo, name='editar_articulo'),
    path('eliminar-articulo/',EliminarArticulo, name='eliminar_articulo'),
    path('<int:pk>/<str:title>/',DetalleArticulo, name='detalle_articulo'),
    path('comentario/',Comentar, name='nuevo_comentario'),
    path('sub-comentario/',SubComentar, name='nuevo_subcomentario'),
]