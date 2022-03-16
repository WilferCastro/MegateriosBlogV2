from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,TemplateView
from .form import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
# Create your views here.

#Pagina principal con los articulos
def Articulos(request):
    return render(request,"principal/articulos.html")

class InicioSesion(LoginView):
    template_name = 'principal/login.html'


class Registro(CreateView):
    model = User
    template_name="principal/registro.html"
    form_class=UserForm
    success_url=reverse_lazy('articulos')
    
    
class NuevoArticulo(LoginRequiredMixin,CreateView):
    model = Article
    form_class=ArticleForm
    template_name="articulos/nuevo_articulo.html"
    success_url=reverse_lazy('articulos')