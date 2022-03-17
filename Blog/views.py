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
    articles = Article.objects.select_related('author').order_by('-id')
    return render(request,"principal/articulos.html",{'articles': articles})

class InicioSesion(LoginView):
    template_name = 'principal/login.html'


@login_required
def MisArticulos(request, id_eje):
    #take care --> -_-
    print(id_eje)
    articles=Article.objects.filter(author_id=id_eje).order_by('-id')
    return render(request,"articulos/mis_articulos.html", {'articles': articles})


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
    
    
class EditarArticulo(LoginRequiredMixin,UpdateView):
    model = Article
    form_class=ArticleForm
    template_name="articulos/editar_articulo.html"
    context_object_name = 'article'
    success_url=reverse_lazy('articulos')
    
    
class EliminarArticulo(LoginRequiredMixin,DeleteView):
    #take care --> -_-
    model = Article
    template_name="articulos/eliminar_articulo.html"
    context_object_name = 'article'
    success_url=reverse_lazy('articulos')