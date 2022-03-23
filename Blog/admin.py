from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import ArticleLikes, CommentLikes, SubComment, User,Article,Comment
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display=("id","author","title","date","likes","dislikes","comments")

class CommentAdmin(admin.ModelAdmin):
    list_display=("id","author","article","comment")
    
class SubCommentADmin(admin.ModelAdmin):
    list_display=("id","commentFather","author","article","subcomment")
    
class ArticleLike(admin.ModelAdmin):
    list_display=("id","author","article","value")
    
admin.site.register(User)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(SubComment,SubCommentADmin)
admin.site.register(ArticleLikes,ArticleLike)
admin.site.register(CommentLikes)