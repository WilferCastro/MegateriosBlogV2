from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,TemplateView
from .form import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
import datetime
# Create your views here.


# def Articulos(request):
#     articles = Article.objects.select_related('author').order_by('-id')
    
#     return render(request,"principal/articulos.html",{'articles': articles})

class Articulos(View):
    
    def get (self, request):
        articles = Article.objects.select_related('author').order_by('-id')
        return render(request,"principal/articulos.html",{'articles':articles})
    

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
 
 
class EliminarArticulo(LoginRequiredMixin, View):
    
    def get(self,request):
        article_id=request.GET.get('id_article')
        article=get_object_or_404(Article,id=article_id)
        #article.delete()
        data = {'article_id': article_id}
        
        return JsonResponse(data)
  

def DetalleArticulo(request,title,pk):
    article=get_object_or_404(Article,id=pk)
    articleLikes=""
    if ArticleLikes.objects.filter(article_id=pk,author_id=request.user.id):
        articleLikes=ArticleLikes.objects.get(article_id=pk,author_id=request.user.id)
    
    return render(request, 'articulos/detalle.html', {'article': article,'articleLikes':articleLikes})


class Comentar(LoginRequiredMixin, View):
    
    def get(self,request):
        author_id=request.GET.get('author')
        article_id=request.GET.get('article')
        com=request.GET.get('comment')
            
        com=Comment.objects.create(author_id=author_id,article_id=article_id,comment=com)
        article=get_object_or_404(Article,id=article_id)
        article.comments+=1
        article.save()
        date=com.date.strftime("%Y-%m-%d")
        data = {'id':com.id,'comment':com.comment,'author':com.author.username,'image':com.author.image.url,'date':date}
            
        return JsonResponse(data)
    
class EditarComentarios(LoginRequiredMixin, View):
    
    def get(self,request):
        value = request.GET.get('value')
        id_comment = request.GET.get('id_comment')
        id_author=request.GET.get('author')
        id_article=request.GET.get('article')
        com=request.GET.get('comment')
        data={'action':'comment'}
        if value == '0':
            comment =Comment.objects.get(id=id_comment,article_id=id_article,author_id=id_author)
            comment.comment=com
            comment.save()
        else:
            data['action']='subcomment'
            print("LO VAMOS A EDITAR SUBCOMMENT XD ")
            
        return JsonResponse(data)
    
    
class EliminarComentarios(LoginRequiredMixin, View):
    
    def get(self,request):
        value = request.GET.get('value')
        id_comment = request.GET.get('id_comment')
        id_author=request.GET.get('author')
        id_article=request.GET.get('article')
        data={'action':'comment'}
        if value == '0':
            comment =Comment.objects.get(id=id_comment,article_id=id_article,author_id=id_author)
            comment.delete()
        else:
            data['action']='subcomment'
            print("LO VAMOS A ELIMINAR SUBCOMMENT XD ")
            
        return JsonResponse(data)
 
        
class SubComentar(LoginRequiredMixin, View):
    
    def get(self,request):
        author_id=request.GET.get('author')
        article_id=request.GET.get('article')
        com=request.GET.get('comment')
        father_id=request.GET.get('father')
        
        com=SubComment.objects.create(author_id=author_id,article_id=article_id,commentFather_id=father_id,subcomment=com)
        article=get_object_or_404(Article,id=article_id)
        article.comments+=1
        article.save()
        date=com.date.strftime("%Y-%m-%d")
        data = {'father': father_id,'comment':com.subcomment,'author':com.author.username,'image':com.author.image.url,'date':date}
        return JsonResponse(data)
        

@login_required
def ArticleLike(request):
    author_id=request.user.id
    article_id=request.GET.get('id_article')
    value = request.GET.get('value')
    article=get_object_or_404(Article,id=article_id)
    articleLikes=""
    
    if ArticleLikes.objects.filter(article_id=article_id,author_id=author_id):
        articleLikes=ArticleLikes.objects.get(article_id=article_id,author_id=author_id)
        
        if articleLikes.value == 0:
            #No hay un like registrado y se le asigna uno
            articleLikes.value=1
            articleLikes.save()
            article.likes+=1
            article.save()
            articleLikes="Like"
        elif articleLikes.value == 1:
            #Ya hay un like registrado y se remueve
            articleLikes.value=0
            articleLikes.save()
            article.likes-=1
            article.save()
            articleLikes="None"
        elif articleLikes.value == 2:
            #Si hay un dislike registrado, re remueve y se agrega un like
            articleLikes.value=1
            articleLikes.save()
            article.dislikes-=1
            article.likes+=1
            article.save()   
            articleLikes="DislikeRemove" 
                  
    else:
        articleLikes=ArticleLikes.objects.create(article_id=article_id,author_id=author_id,value=value)
        articleLikes.value=value
        articleLikes.save()
        article.likes+=1
        article.save()
        articleLikes="Like" 
        
    data = {'like': articleLikes,'likes':article.likes,'dislikes':article.dislikes}
    return JsonResponse(data)


@login_required
def ArticleDislike(request):
    author_id=request.user.id
    article_id=request.GET.get('id_article')
    value = request.GET.get('value')
    article=get_object_or_404(Article,id=article_id)
    articleLikes=""
    
    if ArticleLikes.objects.filter(article_id=article_id,author_id=author_id):
        articleLikes=ArticleLikes.objects.get(article_id=article_id,author_id=author_id)
        
        if articleLikes.value == 0:
            #No hay un dislike registrado y se le asigna uno
            articleLikes.value=2
            articleLikes.save()
            article.dislikes+=1
            article.save()
            articleLikes="Dislike"
        elif articleLikes.value == 2:
            #Ya hay un dislike registrado y se remueve
            articleLikes.value=0
            articleLikes.save()
            article.dislikes-=1
            article.save()
            articleLikes="None"
        elif articleLikes.value == 1:
            #Si hay un like registrado, re remueve y se agrega un dislike
            articleLikes.value=2
            articleLikes.save()
            article.likes-=1
            article.dislikes+=1
            article.save()    
            articleLikes="LikeRemove"
                  
    else:
        articleLikes=ArticleLikes.objects.create(article_id=article_id,author_id=author_id,value=value)
        articleLikes.value=value
        articleLikes.save()
        article.dislikes+=1
        article.save()
        articleLikes="Dislike"
    
    data = {'like': articleLikes,'likes':article.likes,'dislikes':article.dislikes}
    return JsonResponse(data)


@login_required
def CommentLike(request,value,pk,title,pka):
    author_id=request.user.id
    comment=get_object_or_404(Comment,id=pk)
    commentLikes=""
    
    if CommentLikes.objects.filter(comment_id=pk,author_id=author_id):
        commentLikes=CommentLikes.objects.get(comment_id=pk,author_id=author_id)
        
        if commentLikes.value == 0:
            #No hay un like registrado y se le asigna uno
            commentLikes.value=1
            commentLikes.save()
            comment.likes+=1
            comment.save()
        elif commentLikes.value == 1:
            #Ya hay un like registrado y se remueve
            commentLikes.value=0
            commentLikes.save()
            comment.likes-=1
            comment.save()
        elif commentLikes.value == 2:
            #Si hay un dislike registrado, re remueve y se agrega un like
            commentLikes.value=1
            commentLikes.save()
            comment.dislikes-=1
            comment.likes+=1
            comment.save()    
                  
    else:
        commentLikes=CommentLikes.objects.create(comment_id=pk,author_id=author_id,value=value)
        commentLikes.value=value
        commentLikes.save()
        comment.likes+=1
        comment.save()
    
    return redirect("detalle_articulo",title=title, pk=pka)


@login_required
def CommentDislike(request,value,pk,title,pka):
    author_id=request.user.id
    comment=get_object_or_404(Comment,id=pk)
    commentLikes=""
    
    if CommentLikes.objects.filter(comment_id=pk,author_id=author_id):
        commentLikes=CommentLikes.objects.get(comment_id=pk,author_id=author_id)
        
        if commentLikes.value == 0:
            #No hay un dislike registrado y se le asigna uno
            commentLikes.value=2
            commentLikes.save()
            comment.dislikes+=1
            comment.save()
        elif commentLikes.value == 2:
            #Ya hay un dislike registrado y se remueve
            commentLikes.value=0
            commentLikes.save()
            comment.dislikes-=1
            comment.save()
        elif commentLikes.value == 1:
            #Si hay un like registrado, re remueve y se agrega un dislike
            commentLikes.value=2
            commentLikes.save()
            comment.likes-=1
            comment.dislikes+=1
            comment.save()    
                  
    else:
        commentLikes=CommentLikes.objects.create(comment_id=pk,author_id=author_id,value=value)
        commentLikes.value=value
        commentLikes.save()
        comment.dislikes+=1
        comment.save()
    
    return redirect("detalle_articulo",title=title, pk=pka)
