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
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from datetime import date, datetime
from smtplib import SMTPException
from django.http import JsonResponse
from .models import Empleado

# Aqui las vistas
def vistaInicio(request):
    return render(request, "index.html")

def vistaCitas(request):
    return render(request, "CITAS.html")

def vistaCodigo(request):
    return render(request, "codigoRecuperar.html")

def vistaAdministrador(request):
    return render(request, "Administrador/index.html")

def vistaUsuario(request):
    return render(request, "indexUsuario.html")

def vistaPerfilUsuario(request):
    return render(request, "perfilUsuario.html")

def vistaRecuperarContra(request):
    return render(request, "RecuperarContraseña.html")

def vistaRegistrarse(request):
    retorno = {"identificacion": tipoDocumento}
    return render(request, "Registrarse.html", retorno)

def vistConNueva(request):
    return render(request, "DigitarContraseñaNueva.html")

def vistaAdministrador(request):
    return render(request, "Administrador/index.html")

def perfiladmin(request):
    return render(request, "Administrador/perfiladmin.html")

def VistaAgregarEmpleado(request):
    return render(request, "Administrador/frmagregarempleado.html")


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
            
            mensajes = "Felicitaciones, Eres un nuevo usuario, Ya puedes Iniciar Sesion"
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
    retorno = {"mensaje": mensajes, "estado": estado}  
    return render(request,"Registrarse.html",retorno)


def IniciarSesion(request):
    try:
        with transaction.atomic():
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
    except Error as erro:
        transaction.rollback()
        print(erro)
    

def VerificarCorreo(request):
    try:
        correo =  request.POST['txtCorreo']
        Usuario = None
        with transaction.atomic():
            Usuario = User.objects.get(email = correo)
            if Usuario != None:
                codigo = random.randint(0, 99999)
                Usuario.userCodigo = codigo
                Usuario.save()
                asunto='Recuperar Cuenta Sistema Veterinaria Animalagro'
                mensaje=f'Cordial saludo, <b>{Usuario.first_name} {Usuario.last_name}</b>, nos permitimos,\
                    informarle que este es el codigo de recuperacion de su cuenta.\
                    Porfavor No responder este mensaje, este Codigo es unico, No lo comparta.<br>\
                    <br><b>Codigo: </b> {codigo}'
                thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, Usuario.email) )
                thread.start()
                print(Usuario.pk)
                retorno = {"id": Usuario.pk}
                return render(request,'codigoRecuperar.html', retorno )               
            else:
                mensaje = "Correo Incorrecto"
                error = "error"
                titulo ="ERROR"
                return render(request, "RecuperarContraseña.html",{"mensaje":mensaje},{"error":error, "titulo":titulo} )
    except Error as erro:
        transaction.rollback()
        print(erro)
        
    mensaje = "Correo Incorrecto"
    error = "error"
    return render(request, "RecuperarContraseña.html",{"mensaje":mensaje},{"error":error} )
        
def verificarCodigo(request, id):
    try:
        with transaction.atomic():            
            Usuario = None
            codigo = None
            codigo =  int(request.POST.get('txtCodigo'))
            Usuario = User.objects.get(pk = id)
            if Usuario != None:
                if codigo != None:
                    cod = int(Usuario.userCodigo)
                    if codigo == cod:
                        return render(request,'DigitarContraseñaNueva.html', {'id': Usuario.pk})
                    else: 
                        mensaje = "Codigo Incorrecto"
                        error = "error"
                        titulo = "Faltan Datos"
                        return render(request, 'codigoRecuperar.html', {'id': Usuario.pk, 'mensaje': mensaje, 'error': error, 'titulo':titulo} )                        
                else:
                    mensaje="Digita todos los datos"
                    error = "error"
                    titulo = "Faltan Datos"
                    return render(request,'codigoRecuperar.html', {'id': Usuario.pk, 'mensajes': mensaje, 'error': error, 'titulo':titulo} )                        
            else:
                mensaje = "Correo Usuario No Existe"
                error = "error"
                titulo = "Erro Al Verfificar"
                return redirect('/vistaRecuperarContra/',{"mensaje":mensaje},{"error":error} )
            
    except Error as erro:
        transaction.rollback()
        print(erro)

def RegistrarNuevaContraseña(request, id):
    try:
        with transaction.atomic():
            usuario = None
            contraseña = None
            contraseña =  request.POST['txtContraseña']
            usuario = User.objects.get(pk = id)
            if usuario != None:
                if contraseña != None:
                    
                    usuario.set_password(contraseña)
                    usuario.userCodigo = None
                    usuario.save()
                    asunto='Recuperacion De CuentaSistema Veterinaria Animalagro'
                    mensaje=f'Cordial saludo, <b>{usuario.first_name} {usuario.last_name}</b>, nos permitimos,\
                        informarle que usted ha hecho el proceso de recuperacion de su cuenta de forma \
                        exitosa, ya puedes volver Iniciar Sesion\
                        Nos permitimos enviarle las credenciales actualizada de Ingreso a nuestro sistema.<br>\
                        <br><b>Username: </b> {usuario.username}\
                        <br><b>Password: </b> {contraseña}'
                    thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, usuario.email) )
                    thread.start()
                    mensaje = "Recuperaste Tu contraseña Con Exito"
                    tema = "success"
                    titulo = "Felicitaciones"
                    return redirect('/inicio/', {'mensaje': mensaje}, {'tema': tema}, {'titulo':titulo} )                 
                else:
                    mensaje = "Digita La Contraseña"
                    error = "error"
                    titulo = "Faltan Datos"
                    return redirect('/vistaConNueva/', {'id': usuario.pk}, {'mensaje': mensaje}, {'error': error}, {'titulo':titulo} )        
        
    except Error as erro:
         transaction.rollback()
    
# Aqui las funciones que retornan JSON

################################################################
#Bloque De Codigo para El Apartado De Contactos

def registrarContactos(request):
    nombreCon = request.POST["txtNombreCon"]
    emailCon = request.POST["txtEmailCon"]
    numeroCon = int(request.POST["txtNumeroCon"])
    mensajeCon = request.POST["txtMensajeCon"]
    try:
        #Creamos el Contactos
        contac = Contactanos(conNombre = nombreCon, conEmail = emailCon, conNumeroTe = numeroCon,
                           conMensaje =mensajeCon)
        contac.save()
        mensaje="Solicitud De Contacto Enviado Correctamente"
    
    except Error as error:
        mensaje =f"Problemas Al Enviar La Solicitud De Contacto. {error}"

    retorno = {"mensaje": mensaje, "contac": contac}
    return render(request,"index.html", retorno)

################################################################
#Bloque de codigo para agregar un empleado 
def vistaAgregarEmpleado(request):
    if request.method == 'POST':
        nombreE = request.POST["txtNombreEm"]
        apellidoE = request.POST["txtApellidoEm"]
        telefonoE = int(request.POST["txtTelefonoEm"])
        direccionE = request.POST["txtDireccionEm"]
        tipoDocE = request.POST["txtTipoDocEm"]
        numeroDocE = int(request.POST["txtNumeroDocEm"])
        cargoE = request.POST["txtCargoEm"]
        correoE = request.POST["txtCorreoEm"]

    try:
        empleado = Empleado(emNombre = nombreE, emApellido =apellidoE, emTelefono=telefonoE, 
                            emDireccion=direccionE,emTipoDoc=tipoDocE,
                            emNumeroDoc=numeroDocE, emCargo=cargoE, emCorreo=correoE)
        empleado.save()
        mensaje ="Empleado agregado correctamente"
        return redirect("/listarEmpleados/")
    except Error as error:
        mensaje=f"Problemas al agregar empleado. {error}"

    retorno = {"mensaje":mensaje, "empleado":empleado}
    return render(request,"Administrador/frmagregarempleado.html", retorno)



def listarEmpleados(request):
    try: 
        empleados = Empleado.objects.all()
        mensaje=""
        print(empleados)
    except:
        mensaje="Problemas al obtener los empleados"
    retorno = {"mensaje":mensaje, "listarEmpleados":empleados}
    return render(request,"Administrador/listaempleados.html", retorno)

########################################################################
#Bloque De Codigo Para Agregar Proveedor

def VistaRegistrarProveedor(request):
    if request.method == 'POST':
        try:
            # Traemos los datos del formulario de proveedor
            NombreP = request.POST.get("txtNombrePro")
            NombreRepresentante = request.POST.get("txtNombreRepre")
            DireccionEmpresa = request.POST.get("txtDireccionPro")
            TelefonoProveedor = int(request.POST.get("txtTelefonoPro"))
            NitEmpresa = int(request.POST.get("txtNitPro"))
            
            # Creamos un proveedor
            proveedor = Proveedor(
                proNombre=NombreP,
                proRepresentante=NombreRepresentante,
                proDireccion=DireccionEmpresa,
                proTelefono=TelefonoProveedor,
                proNit=NitEmpresa
            )
            # Guardamos el proveedor en la base de datos
            proveedor.save()
            mensaje = "Proveedor agregado correctamente"
        except Exception as error:
            mensaje = f"Error: {str(error)}"
    else:
        mensaje = ""
        proveedor = None
    
    retorno = {"mensaje": mensaje, "provedor": proveedor}
    return render(request, "Administrador/frmAgregarProveedor.html", retorno)

##########################################################
#Bloque de codigo para guardar la categoria
def VistaRegistrarCategoria(request):
    if request.method == 'POST':
        try:
            NombreCategoria = request.POST.get("txtNombreCat")
            #Creamos una categoria
            categoria = Categoria(catNombre=NombreCategoria)
            # Guardamos el proveedor en la base de datos
            categoria.save()
            mensaje = "Categoria agregada correctamente"
        
        except Exception as error:
            mensaje = f"Error: {str(error)}"
    else:
        mensaje = ""
        categoria= None
    
    retorno = {"mensaje": mensaje}
    return render(request, "Administrador/frmAgregarProveedor.html", retorno)

#####################################################################
#Bloque De Codigo Para Guardar Los Productos


def VistaProductos(request):
    proveedores = Proveedor.objects.all()
    categorias = Categoria.objects.all()
    es = estadoProducto
    retorno = {"proveedores": proveedores, "categorias": categorias, "estados": es}
    print(retorno)
    return render(request, "Administrador/frmAgregarProveedor.html", retorno)


def RegistrarProducto(request):
    if request.method == 'POST':
        estado = False
        try:
            with transaction.atomic():
                # Traemos los datos del formulario de productos
                nombre_producto = request.POST.get("txtNombreP")
                estado_pro = request.POST.get("cbEstado")
                precio_producto = int(request.POST.get("txtPrecioP"))
                archivo = request.FILES.get("fileFoto")
                descripcion_producto = request.POST.get("txtDescripcionP")
                id_proveedor = int(request.POST.get('cbProvedor'))
                id_categoria = int(request.POST.get('cbCategoria'))
                cat_recibe = Categoria.objects.get(pk=id_categoria)
                pro_recibe = Proveedor.objects.get(pk=id_proveedor)

                # Creamos un producto
                producto = Producto(
                    proNombre=nombre_producto,
                    proEstado=estado_pro,
                    proPrecio=precio_producto,
                    proDescripcion=descripcion_producto,
                    proFoto=archivo,
                    proProveedor=pro_recibe,
                    proCategoria=cat_recibe
                )
                producto.save()
                estado = True
                titulo = "Agregado Correctamente"
                mensaje = "Se ha registrado el producto correctamente"
                tema = "success"

        except Error as error:
            transaction.rollback()
            mensaje = str(error)

        retorno = {"estado": estado, "mensaje": mensaje, "titulo": titulo, "tema": tema}
        return render(request, "Administrador/frmAgregarProveedor.html", retorno)
