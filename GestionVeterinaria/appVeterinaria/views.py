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


# Aqui las funciones que retornan JSON

def registrarseUsuario(request):
    try: 
        estado = False
        mensaje = ""
        datos = json.loads(request.body)
        with transaction.atomic():
            usuario = User(userTipoDoc = datos["tipoIde"],  userNoDoc = datos["identificacion"], userTelefono = datos["Telefono"],
                        userTipo = "Usuario", first_name = datos["nombre"], last_name = datos["apellido"], email = datos["correo"],
                        username = datos["correo"])
            usuario.save()
            rol = Group.objects.get(pk=1)
            usuario.groups.add(rol)
            if(rol.name=="Administrador"):usuario.is_staff = True
            usuario.save()
            print(datos["contraseña"])
            usuario.set_password(datos["contraseña"])
            usuario.save()
            
            mensaje = "Felicitaciones, eres un nuevo usuario, Bienvenido a nuestra"
            retorno = {"mensaje": mensaje}
            asunto='Registro Sistema Veterinaria Animalagro'
            mensaje=f'Cordial saludo, <b>{usuario.first_name} {usuario.last_name}</b>, nos permitimos.\
                informarle que usted ha sido registrado en el Sistema de nuestra veterinaria Animalagro \
                ubicada en campoalegre, Huila, ubicada Ca 12 calle 18.\
                Nos permitimos enviarle las credenciales de Ingreso a nuestro sistema.<br>\
                <br><b>Username: </b> {usuario.username}\
                <br><b>Password: </b> {datos["contraseña"]}\
                '
            thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, usuario.email) )
            thread.start()
    except Error as error:
        print(error)