from datetime import timezone
import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,TemplateView
from .form import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
# Create your views here.

def Articulos(request):
    articles = Article.objects.select_related('author').order_by('-id')
    print(datetime.datetime.now(timezone.utc))
    
    #for i in articles:
        #print(i.date.strftime("%H:%M:%S"))
        # for j in i.comment_set.all():
        #     print("-----------------------------------------------------")
        #     print(j)
        #     print("Titulo del articulo: ",j.article)
        #     print("Autor del comentario: ",j.author.username)
        #     print("Comentarios: ",j.comment)
        #     print("-----------------------------------------------------\n")
    
    return render(request,"principal/articulos.html",{'articles': articles})

class InicioSesion(LoginView):
    template_name = 'principal/login.html'


@login_required
def MisArticulos(request, pk):
    if request.user.id == pk:
        articles=Article.objects.filter(author_id=pk).order_by('-id')
        return render(request,"articulos/mis_articulos.html", {'articles': articles})
    else:
        return render(request,"articulos/error.html")

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
  
@login_required
def EditarArticulo(request,pk):
    #Obtener id del usuario logueado
    user_id=request.user.id
    #Obtener todos los articulos de dicho usuario
    articles_id=Article.objects.filter(author_id=user_id)
    #Crear y llenar la lista con los id de los articulos relacionados con el usuario 
    li=[]
    for i in articles_id:
       li.append(i.id)
       
    print(li)
    #Si el usuario cambia el id por un articulo que no es suyo, se renderiza el error,
    #caso contrario se renderizará la pagina con el articulo seleccionado
    if request.method == 'GET':
        if pk in li:
            article=Article.objects.get(id=pk)
            return render(request,"articulos/editar_articulo.html",{'article': article})
        else:
            return render(request,"articulos/error.html")
        
    #Cuando el usuario envia el formulario
    elif request.method == 'POST':
        article=Article.objects.get(id=pk)
        article.title=request.POST['title']
        article.photo=request.FILES['photo']
        article.introduction=request.POST['introduction']
        article.content=request.POST['content']
        article.save()
        return redirect("mis_articulos", pk=user_id)
    
# class EditarArticulo(LoginRequiredMixin,UpdateView):
#     model = Article
#     form_class=ArticleForm
#     template_name="articulos/editar_articulo.html"
#     context_object_name = 'article'
#     success_url=reverse_lazy('articulos')
    
    
@login_required
def EliminarArticulo(request):
    #take care --> -_-
    article_id=request.GET.get("id_article")
    user_id=request.user.id
    
    article=Article.objects.get(id=article_id)
    article.delete()
    return redirect("mis_articulos", pk=user_id)


def DetalleArticulo(request,title,pk):
    article=Article.objects.get(id=pk)
    
    return render(request, 'articulos/detalle_articulo.html', {'article': article})

@login_required
def Comentar(request):
    aut=request.POST['author']
    art=request.POST['article']
    com=request.POST['comment']
    tit=request.POST['title']
    
    Comment.objects.create(author_id=aut,article_id=art,comment=com)
    return redirect("detalle_articulo", title=tit, pk=art)

    