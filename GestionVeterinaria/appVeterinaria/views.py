from django.shortcuts import render
from django.shortcuts import render,redirect
from appVeterinaria.models import *
from django.contrib.auth.models import Group
from django.db import Error,transaction
import random
import string
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings
import urllib
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from datetime import date, datetime
from smtplib import SMTPException
from django.http import JsonResponse

# Aqui las vistas
def vistaInicio(request):
    return render(request, "index.html")

def vistaCitas(request):
    return render(request, "CITAS.html")

def vistaCodigo(request):
    return render(request, "codigoRecuperar.html")

def vistaAdministrador(request):
    return render(request, "indexe.html")

def vistaUsuario(request):
    return render(request, "indexUsuario.html")

def vistaPerfilUsuario(request):
    return render(request, "perfilUsuario.html")

def vistaRecuperarContra(request):
    return render(request, "recuperarContraseña.html")

def vistaRegistrarse(request):
    retorno = {"identificacion": tipoDocumento}
    return render(request, "Registrarse.html", retorno)


# Aqui las vistas Gestion, son las que se cargan con datos o tienen Tablas 




# Aqui los metodos o funciones que no retornan JSON

def enviarCorreo (asunto=None, mensaje=None, destinatario=None): 
    remitente = settings.EMAIL_HOST_USER 
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'destinatario': destinatario,
        'mensaje': mensaje,
        'asunto': asunto,
        'remitente': remitente,
    })
    try:
        correo = EmailMultiAlternatives (asunto, mensaje, remitente, [destinatario]) 
        correo.attach_alternative (contenido, 'text/html') 
        correo.send(fail_silently=True)
    except SMTPException as error: 
        print(error)


def registrarseUsuario(request):
    try: 
        estado = False
        mensaje = ""
        tipoDoc = request.POST.get('cbIdentificacioon')
        identificacion = request.POST.get('txtIdentificacion')
        telefono = request.POST.get('txtTelefono')
        nombre = request.POST.get('txtNombre')
        apellido = request.POST.get('txtApellido')
        email =  request.POST.get('txtCorreo')
        contraseña = request.POST.get('txtContraseña')
        with transaction.atomic():
            usuario = User(userTipoDoc = tipoDoc,  userNoDoc = identificacion, userTelefono = telefono,
                        userTipo = "Usuario", first_name = nombre, last_name = apellido , email = email,
                        username = email)
            usuario.save()
            rol = Group.objects.get(pk=1)
            usuario.groups.add(rol)
            if(rol.name=="Administrador"):usuario.is_staff = True
            usuario.save()
            print(contraseña)
            usuario.set_password(contraseña)
            usuario.save()
            
            mensaje = "Felicitaciones, eres un nuevo usuario, Bienvenido a nuestra"
            retorno = {"mensaje": mensaje}
            asunto='Registro Sistema Veterinaria Animalagro'
            mensaje=f'Cordial saludo, <b>{usuario.first_name} {usuario.last_name}</b>, nos permitimos,\
                informarle que usted ha sido registrado en el Sistema de nuestra veterinaria Animalagro \
                ubicada en campoalegre, Huila, ubicada Ca 12 calle 18.\
                Nos permitimos enviarle las credenciales de Ingreso a nuestro sistema.<br>\
                <br><b>Username: </b> {usuario.username}\
                <br><b>Password: </b> {contraseña}'
            thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, usuario.email) )
            thread.start()
            estado = True
    except Error as error:
        transaction.rollback()
        print(error)
    retorno = {"mensaje": mensaje, "estado": estado}  
    return render(request,"Registrarse.html",retorno)

def IniciarSesion(request):
    usernamee= request.POST["txtUsuario"] 
    passworde = request.POST["txtContraseña"]
    user = authenticate(username=usernamee, password=passworde)
    print (user)
    if user is not None:
        #registrar la variable de sesión
        auth.login(request, user)
        if user.groups.filter(name='Usuario').exists():
            return redirect('/vistaIndexUsuario/')
        elif user.groups.filter(name='Asistente').exists():
            return redirect('/inicio/')
        else:
            return redirect('/inicio/')
    else:
        mensaje = "Usuario o Contraseña Incorrectas"
        return render(request, "index.html",{"mensaje":mensaje})
    
    
# Aqui las funciones que retornan JSON