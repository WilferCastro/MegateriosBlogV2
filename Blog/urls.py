from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',Articulos, name='articulos'),
    path('iniciar-sesion/',Login, name='login'),
    path('registrarme/',Registro, name='registro'),
    #path('principal/',Principal, name='principal'),
]