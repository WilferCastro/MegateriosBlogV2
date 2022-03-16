from dataclasses import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'image',
        ]

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
            'username': forms.TextInput(attrs={'class': 'w3-input'}),
            'first_name': forms.TextInput(attrs={'class': 'w3-input'}),
            'last_name': forms.TextInput(attrs={'class': 'w3-input'}),
            'email': forms.EmailInput(attrs={'class': 'w3-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'w3-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'w3-input'}),
        }
        
        
        
        
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = [
            'title',
            'photo',
            'introduction',
        ]

        labels = {
            'title': 'Titulo del articulo',
            'photo': 'Imagen del articulo',
            'introduction': 'Abrebocas',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input'}),
            'introduction': forms.TextInput(attrs={'class': 'w3-input'}),
        }