from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .form import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
# Create your views here.

class Articulos(View):
    
    def get (self, request):
        articles = Article.objects.all()
        return render(request,"principal/articulos.html",{'articles':articles})
    
    
class InicioSesion(View):
    
    def get(self,request):
        return render(request, 'principal/login.html')
    
    def post(self,request):
        us=request.POST.get("username")
        pas=request.POST.get("password")
        user = authenticate(username=us, password=pas)
        if user is not None:
            login(request,user)
            return JsonResponse({"ok":'oj'})
        else:
            return JsonResponse({"error":"Verifique su usuario y contraseña e intente nuevamente."})


class MisArticulos(LoginRequiredMixin,View):
    
    def get(self,request,pk):
        if request.user.id == pk:
            articles=Article.objects.filter(author_id=pk).order_by('-id')
            return render(request,"articulos/mis_articulos.html", {'articles': articles})
        else:
            return render(request,"articulos/error.html")


class Registro(View):
    
    def get(self,request):
        return render(request,"principal/registro.html")
    
    def post(self,request):
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({"ok":"oj"})
        else:
            return JsonResponse(form.errors, status=400)

    
class NuevoArticulo(LoginRequiredMixin,CreateView):
    model = Article
    form_class=ArticleForm
    template_name="articulos/nuevo_articulo.html"
    success_url=reverse_lazy('articulos')
  
  
@login_required
def EditarArticulo(request,pk):
    user_id=request.user.id
    articles_id=Article.objects.filter(author_id=user_id)
    li=[]
    for i in articles_id:
       li.append(i.id)
       
    if request.method == 'GET':
        if pk in li:
            article=get_object_or_404(Article,id=pk)
            return render(request,"articulos/editar_articulo.html",{'article': article})
        else:
            return render(request,"articulos/error.html")
        
    elif request.method == 'POST':
        article=get_object_or_404(Article,id=pk)
        article.title=request.POST['title']
        article.photo=request.FILES['photo']
        article.introduction=request.POST['introduction']
        article.content=request.POST['content']
        article.save()
        return redirect("mis_articulos", pk=user_id)
 
 
class EliminarArticulo(LoginRequiredMixin, View):
    
    def post(self,request):
        article_id=request.POST.get('id_article')
        article=get_object_or_404(Article,id=article_id)
        #article.delete()
        data = {'article_id': article_id}
        
        return JsonResponse(data)
  
  
class DetalleArticulo(View):
    
    def get(self,request,title,pk):
        article=get_object_or_404(Article,id=pk)
        com=Comment.objects.filter(article_id=pk).count()
        sub=SubComment.objects.filter(article_id=pk).count()
        total_comments=com+sub
        articleLikes=""
        if ArticleLikes.objects.filter(article_id=pk,author_id=request.user.id):
            articleLikes=ArticleLikes.objects.get(article_id=pk,author_id=request.user.id)
        
        return render(request, 'articulos/detalle.html', {'article': article,'articleLikes':articleLikes,'total_comments':total_comments})
    

class Comentar(LoginRequiredMixin, View):
    
    def post(self,request):
        author_id=request.POST.get('author_id')
        article_id=request.POST.get('article_id')
        com=request.POST.get('comment')
        
        com=Comment.objects.create(author_id=author_id,article_id=article_id,comment=com)
        date=com.date.strftime("%d-%m, %Y")
        data = {'id':com.id,'comment':com.comment.capitalize(),'author':com.author.username,'image':com.author.image.url,'date':date}
            
        return JsonResponse(data)
    
    
class EditarComentarios(LoginRequiredMixin, View):
    
    def post(self,request):
        value = request.POST.get('evalue')
        id_comment = request.POST.get('eid_comment')
        id_article = request.POST.get('article_id')
        com=request.POST.get('comment_text')
        data={'action':'comment'}
        if value == '0':
            comment =Comment.objects.get(id=id_comment,article_id=id_article)
            comment.comment=com
            comment.edited=True
            comment.save()
        else:
            comment =SubComment.objects.get(id=id_comment,article_id=id_article)
            comment.subcomment=com
            comment.edited=True
            comment.save()
            data['action']='subcomment'
            
        return JsonResponse(data)
    
    
class EliminarComentarios(LoginRequiredMixin, View):
    
    def post(self,request):
        value = request.POST.get('dvalue')
        id_comment = request.POST.get('did_comment')
        id_article = request.POST.get('article_id')
        data={'action':'comment'}
        if value == '0':
            comment =Comment.objects.get(id=id_comment,article_id=id_article)
            comment.delete()
        else:
            comment =SubComment.objects.get(id=id_comment,article_id=id_article)
            comment.delete()
            data['action']='subcomment'
            
        return JsonResponse(data)
    
        
class SubComentar(LoginRequiredMixin, View):
    
    def post(self,request):
        author_id=request.POST.get('author_id')
        article_id=request.POST.get('article_id')
        comment_id=request.POST.get('sid_comment')
        com=request.POST.get('subcomment')
        
        com=SubComment.objects.create(author_id=author_id,article_id=article_id,commentFather_id=comment_id,subcomment=com)
        date=com.date.strftime("%d-%m, %Y")
        data = {'id':com.id,'comment_id': comment_id,'comment':com.subcomment.capitalize(),'author':com.author.username,'image':com.author.image.url,'date':date}
        return JsonResponse(data)


class ArticleLike(LoginRequiredMixin,View):
    
    def get(self,request):
        author_id=request.user.id
        article_id=request.GET.get('id_article',2)
        value = request.GET.get('value',1)
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


class ArticleDislike(LoginRequiredMixin,View):
    
    def get(self,request):
        author_id=request.user.id
        article_id=request.GET.get('id_article',None)
        value = request.GET.get('value',1)
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
