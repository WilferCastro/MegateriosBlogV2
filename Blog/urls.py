from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    path('',Articulos, name='articulos'),
    path('accounts/login/',InicioSesion.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('registrarme/',Registro.as_view(), name='registro'),
    path('nuevo-articulo/',NuevoArticulo.as_view(), name='nuevo_articulo'),
]