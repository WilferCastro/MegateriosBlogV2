from dataclasses import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User

        fields = ['username','first_name','last_name','email','password1','password2','image',]

        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo Electronico',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
            'image': 'Seleccione su imagen',
        }

        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
        
        
        
        
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = ['title','photo','introduction','author','content',]

        labels = {
            'title': 'Titulo del articulo',
            'photo': 'Imagen del articulo',
            'introduction': 'Abrebocas',
            'author': 'Autor',
            'content': 'Contenido del articulo',
        }

        widgets = {
            'title': forms.TextInput(),
            'introduction': forms.Textarea(),
            'author': forms.Select(),
            'content': forms.Textarea(),
        }
        