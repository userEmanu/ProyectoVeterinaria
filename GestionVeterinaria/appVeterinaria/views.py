from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, "index.html")

def citas(request):
    return render(request, "CITAS.html")

def codigo(request):
    return render(request, "codigoRecuperar.html")

def administrador(request):
    return render(request, "indexe.html")

def usuario(request):
    return render(request, "indexUsuario.html")

def usuarios(request):
    return render(request, "perfilUsuario.html")

def RecuperarContra(request):
    return render(request, "recuperarContraseña.html")

def Registrarse(request):
    return render(request, "Registrarse.html")
