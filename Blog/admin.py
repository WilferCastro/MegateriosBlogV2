from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import ArticleLikes, CommentLikes, SubComment, User,Article,Comment
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display=("id","author","title","date","likes","dislikes","comments")

class CommentAdmin(admin.ModelAdmin):
    list_display=("id","author","article","comment","likes","dislikes")
    
class SubCommentAdmin(admin.ModelAdmin):
    list_display=("id","commentFather","author","article","subcomment")
    
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display=("id","author","article","value")
    
class CommentLikeAdmin(admin.ModelAdmin):
    list_display=("id","author","comment","value")
    
admin.site.register(User)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(SubComment,SubCommentAdmin)
admin.site.register(ArticleLikes,ArticleLikeAdmin)
admin.site.register(CommentLikes,CommentLikeAdmin)