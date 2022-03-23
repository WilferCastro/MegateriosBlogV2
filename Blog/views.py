from datetime import timezone
import datetime
from django.shortcuts import get_object_or_404, redirect, render
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
            article=get_object_or_404(Article,id=pk)
            return render(request,"articulos/editar_articulo.html",{'article': article})
        else:
            return render(request,"articulos/error.html")
        
    #Cuando el usuario envia el formulario
    elif request.method == 'POST':
        article=get_object_or_404(Article,id=pk)
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
    
    article=get_object_or_404(Article,id=article_id)
    article.delete()
    return redirect("mis_articulos", pk=user_id)


def DetalleArticulo(request,title,pk):
    article=get_object_or_404(Article,id=pk)
    articleLikes=""
    if ArticleLikes.objects.filter(article_id=pk,author_id=request.user.id):
        articleLikes=ArticleLikes.objects.get(article_id=pk,author_id=request.user.id)
    
    return render(request, 'articulos/detalle_articulo.html', {'article': article,'articleLikes':articleLikes})


@login_required
def Comentar(request):
    aut=request.POST['author']
    art=request.POST['article']
    com=request.POST['comment']
    tit=request.POST['title']
    
    article=get_object_or_404(Article,id=art)
    article.comments+=1
    article.save()
    
    Comment.objects.create(author_id=aut,article_id=art,comment=com)
    return redirect("detalle_articulo", title=tit, pk=art)


@login_required
def SubComentar(request):
    fcom=request.POST['sid_comment']
    aut=request.POST['sauthor']
    art=request.POST['sarticle']
    com=request.POST['subcomment']
    tit=request.POST['stitle']
    
    article=get_object_or_404(Article,id=art)
    article.comments+=1
    article.save()
    
    SubComment.objects.create(author_id=aut,article_id=art,commentFather_id=fcom,subcomment=com)
    return redirect("detalle_articulo", title=tit, pk=art)


@login_required
def ArticleLike(request,value,pk):
    author_id=request.user.id
    article=get_object_or_404(Article,id=pk)
    articleLikes=""
    
    if ArticleLikes.objects.filter(article_id=pk,author_id=author_id):
        articleLikes=ArticleLikes.objects.get(article_id=pk,author_id=author_id)
        
        if articleLikes.value == 0:
            #No hay un like registrado y se le asigna uno
            articleLikes.value=1
            articleLikes.save()
            article.likes+=1
            article.save()
        elif articleLikes.value == 1:
            #Ya hay un like registrado y se remueve
            articleLikes.value=0
            articleLikes.save()
            article.likes-=1
            article.save()
        elif articleLikes.value == 2:
            #Si hay un dislike registrado, re remueve y se agrega un like
            articleLikes.value=1
            articleLikes.save()
            article.dislikes-=1
            article.likes+=1
            article.save()    
                  
    else:
        articleLikes=ArticleLikes.objects.create(article_id=pk,author_id=author_id,value=value)
        articleLikes.value=value
        articleLikes.save()
        article.likes+=1
        article.save()
    
    return redirect("detalle_articulo",title=article.title, pk=pk)


@login_required
def ArticleDislike(request,value,pk):
    author_id=request.user.id
    article=get_object_or_404(Article,id=pk)
    articleLikes=""
    
    if ArticleLikes.objects.filter(article_id=pk,author_id=author_id):
        articleLikes=ArticleLikes.objects.get(article_id=pk,author_id=author_id)
        
        if articleLikes.value == 0:
            #No hay un dislike registrado y se le asigna uno
            articleLikes.value=2
            articleLikes.save()
            article.dislikes+=1
            article.save()
        elif articleLikes.value == 2:
            #Ya hay un dislike registrado y se remueve
            articleLikes.value=0
            articleLikes.save()
            article.dislikes-=1
            article.save()
        elif articleLikes.value == 1:
            #Si hay un like registrado, re remueve y se agrega un dislike
            articleLikes.value=2
            articleLikes.save()
            article.likes-=1
            article.dislikes+=1
            article.save()    
                  
    else:
        articleLikes=ArticleLikes.objects.create(article_id=pk,author_id=author_id,value=value)
        articleLikes.value=value
        articleLikes.save()
        article.dislikes+=1
        article.save()
    
    return redirect("detalle_articulo",title=article.title, pk=pk)