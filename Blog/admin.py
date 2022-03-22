from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import User,Article,Comment
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display=("author","title","date","likes","dislikes","comments")

class CommentAdmin(admin.ModelAdmin):
    list_display=("author","article","comment")
    
admin.site.register(User)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)