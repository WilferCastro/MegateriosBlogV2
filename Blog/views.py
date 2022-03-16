from django.shortcuts import render

# Create your views here.

#Pagina principal con los articulos
def Articulos(request):
    return render(request,"principal/articulos.html")



def Login(request):
    return render(request,"principal/login.html")



def Registro(request):
    return render(request,"principal/registro.html")