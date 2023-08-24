from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.shortcuts import render
from django.shortcuts import render,redirect
from appVeterinaria.models import *
from django.contrib.auth.models import Group
from django.db import Error,transaction
import random
import string
import os
from django.contrib.auth import authenticate
from django.contrib import auth
from django.conf import settings
import urllib
import json
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from datetime import date, datetime, time, timedelta
from smtplib import SMTPException
from django.db.models import Sum, Avg, Count
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, FileResponse
from fpdf import FPDF
from appVeterinaria.carrito import *
from appVeterinaria.pdfHistorialClinico import PDF

# Aqui las vistas

def vistaInicio(request, mensaje = ""):
    auth.logout(request)
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):
            return redirect('/vistaIndexUsuario/')
        elif request.user.groups.filter(name='Administrador'):
            return redirect('/vistaAdministrador/')
    else:

        # Obtener todos los objetos del modelo Servicio desde la base de datos
        servicio = Servicio.objects.all()
        pro = Producto.objects.all()
        # Crear un diccionario con la lista de objetos de Servicio y pasarlo a la plantilla
        retorno = {"servicio": servicio, "productos": pro, "mensaje": mensaje}
        return render(request, "index.html", retorno)

def vistaGestionCitas(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):
            return render(request, 'Error/403.html')
        else:
            retorno = {'cita': Cita.objects.all(), 'estado': estadoCita }   
            return render(request,"Administrador/frmGestionCitas.html", retorno)
    else:
        return render(request, 'Error/403.html')
    

def vistaCitaHTML(request, id):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):
            return render(request, 'Error/403.html')
        else:
            retorno = {
                "cita": Cita.objects.get(pk = id)
            }
            return render(request,"Administrador/frmCita.html", retorno)
    else: 
        return render(request, 'Error/403.html')
    

def vistaCitas(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):      
            return render(request, "CITAS.html")
        else:
            return render(request, 'Error/403.html')
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)

def vistaCodigo(request):
    if request.user.is_authenticated:
        return render(request, 'Error/403.html')
    else:
        return render(request, "codigoRecuperar.html")

def vistaGestionServicio(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):      
            return render(request, 'Error/403.html')
        else:
            empleado = {'empleado': Empleado.objects.all(), 'servicio': Servicio.objects.all(),"user": request.user,
                        "rol": request.user.groups.get().name}
            return render(request, 'Administrador/frmGestionServicio.html', empleado)
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)

def vistaAdministrador(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):      
            return render(request, 'Error/403.html')
        else:
            user= {"user": request.user,
                        "rol": request.user.groups.get().name}
            return render(request, "Administrador/index.html",user)
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)

def vistaUsuario(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):      
            user= {"user": request.user,
                       "rol": request.user.groups.get().name, "servicio": Servicio.objects.all()}
            return render(request, "indexUsuario.html", user)
        else:
            return render(request, 'Error/403.html')
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)
    

def vistaPerfilUsuario(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'): 
            use = request.user      
            pedidos = Pedido.objects.filter(peUsuario = use)
            user= {"user": use,
                        "rol": request.user.groups.get().name, "pedido": pedidos}
            print(len(pedidos))
            return render(request, "perfilUsuario.html", user)
        else:
            return render(request, 'Error/403.html')
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)

def vistaRecuperarContra(request):
    if request.user.is_authenticated:      
        return render(request, 'Error/403.html')
    else:     
        return render(request, "RecuperarContraseña.html")

def vistaRegistrarse(request):
    if request.user.is_authenticated:
        return render(request, 'Error/403.html')
    else:
        retorno = {"identificacion": tipoDocumento}
        return render(request, "Registrarse.html", retorno)

def vistConNueva(request):
    if request.user.is_authenticated:
        return render(request, 'Error/403.html')
    else:
        return render(request, "DigitarContraseñaNueva.html")


def perfiladmin(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, 'Error/403.html')
        else:
            return render(request, "Administrador/perfiladmin.html")
    else:
        return render(request, 'Error/403.html')

def VistaAgregarEmpleado(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, 'Error/403.html')
        else:
            return render(request, "Administrador/frmagregarempleado.html")
    else:
        return render(request, 'Error/403.html')
    


# Aqui las vistas Gestion, son las que se cargan con datos o tienen Tablas 

def CerrarSesion(request):
    auth.logout(request)
    return redirect( "/inicio/",
                  {"mensaje":"Has cerrado la sesión"})


# Aqui los metodos o funciones que no retornan JSON

def enviarCorreo(asunto=None, mensaje=None, destinatario=None,archivo=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'destinatario': destinatario,
        'mensaje': mensaje,
        'asunto': asunto,
        'remitente': remitente,
    })
    try:
        correo = EmailMultiAlternatives(
            asunto, mensaje, remitente, [destinatario])
        correo.attach_alternative(contenido, 'text/html')
        if archivo != None:
            correo.attach_file(archivo)
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
        redirect ("/inicio/")
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
                if user.groups.filter(name='Administrador').exists():
                    return redirect('/vistaAdministrador')
                elif user.groups.filter(name='Asistente').exists():
                    return redirect('/inicio')
                else:
                    return redirect('/vistaIndexUsuario')
            else:
                mensaje = "Usuario o Contraseña Incorrectas"
                return redirect(f'/inicio/{mensaje}')
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
                    return redirect(f'/inicio/{mensaje}' )                 
                else:
                    mensaje = "Digita La Contraseña"
                    error = "error"
                    titulo = "Faltan Datos"
                    return redirect('/vistaConNueva/', {'id': usuario.pk}, {'mensaje': mensaje}, {'error': error}, {'titulo':titulo} )        
        
    except Error as erro:
         transaction.rollback()
    
# Aqui las funciones que retornan JSON

# --------------
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
        asunto='Contactanos Sistema Veterinaria Animalagro'
        mensaje=f'Cordial saludo, <b>{nombreCon} </b>, nos permitimos,\
            informarle que usted se ha comunicado con nosotros en el apartado de <b>contactanos </b>\
            pronto nos comuniremos con usted.\
            No responder este mensaje, Nos comunicaremo contigo. <br>'
        thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, emailCon) )
        thread.start()
        mensaje="Solicitud De Contacto Enviado Correctamente"
    
    except Error as error:
        mensaje =f"Problemas Al Enviar La Solicitud De Contacto. {error}"

    retorno = {"mensaje": mensaje, "contac": contac}
    return render(request,"index.html", retorno)

################################################################
#Bloque de codigo para agregar un empleado 
def vistaAgregarEmpleado(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, '403.html')
        else:
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
    else:
        return render(request, 'Error/403.html')


def listarEmpleados(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, 'Error/403.html')
        else:
            try: 
                empleados = Empleado.objects.all()
                mensaje=""
                print(empleados)
            except:
                mensaje="Problemas al obtener los empleados"
            retorno = {"mensaje":mensaje, "listarEmpleados":empleados}
            return render(request,"Administrador/listaempleados.html", retorno)
    else: 
        return redirect('/inicio/')

########################################################################
#Bloque De Codigo Para Agregar Proveedor

def VistaRegistrarProveedor(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, 'Error/403.html')
        else:
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
            retorno = {"mensaje": mensaje, "provedor": proveedor}
            return redirect("/VistaProductos/", retorno)
    else:
        return redirect('/inicio/')

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
    return redirect("/VistaProductos/", retorno)

#####################################################################
#Bloque De Codigo Para Guardar Los Productos


def VistaProductos(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, '403.html')
        else:
            proveedores = Proveedor.objects.all()
            categorias = Categoria.objects.all()
            es = estadoProducto
            retorno = {"proveedores": proveedores, "categorias": categorias, "estados": es}
            print(retorno)
            return render(request, "Administrador/frmAgregarProveedor.html", retorno)
    else:
        return render(request, 'Error/403.html')


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
        return redirect("/VistaProductos/", retorno)

def vistaproductos(request):
    productos = Producto.objects.all()
    carrito = Carrito(request)
    total = carrito.total_carrito()
    return render(request, "productos.html", {'productos':productos, 'total': total})


def agregar_producto(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.agregar(producto)
    return redirect("productos")

def eliminar_producto(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.eliminar(producto)
    return redirect("productos")

def restar_producto(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.restar(producto)
    return redirect("productos")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("productos")

def vistaEmpleadoUsuario(request, id):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, 'Error/403.html')
        else:
            try:
                empleado = Empleado.objects.get(pk = id)
                rol = Group.objects.all()
                retorno = {"empleado": empleado, "rol": rol, "tipo": tiposUsuarios}        
            except Error as e:
                print(e)    
                
            return render(request, "Administrador/registrarUsuarioEmpleado.html", retorno)
    else:
        return render(request, 'Error/403.html')

def CrearUsuarioEmpleado(request, id):
    try:
        tipoUser = request.POST.get('cbTipo')
        rol = request.POST.get('cbRol')
        with transaction.atomic():
            
            em= None
            em = Empleado.objects.get(pk = id)
            if em != None:                
                user = User(userTipoDoc = em.emTipoDoc,  userNoDoc = em.emNumeroDoc, userTelefono = em.emTelefono,
                        userTipo = tipoUser, first_name = em.emNombre, last_name = em.emApellido, email = em.emCorreo,
                        username = em.emCorreo, userEmpleado = em)
                user.save()
                rol = Group.objects.get(pk=rol)
                user.groups.add(rol)
                if(rol.name=="Administrador"):user.is_staff = True
                user.save()
                contraseña = generarPassword()
                print(contraseña)
                user.set_password(contraseña)
                user.save()
                asunto='Registro Usurio De Empleado Sistema Veterinaria Animalagro'
                mensaje=f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos,\
                    informarle que usted ha sido registrado en el Sistema de nuestra veterinaria Animalagro \
                    ubicada en campoalegre, Huila, ubicada Ca 12 calle 18.\
                    Nos permitimos enviarle las credenciales de Ingreso a nuestro sistema.<br>\
                    <br><b>Username: </b> {user.username}\
                    <br><b>Password: </b> {contraseña}'
                thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, user.email) )
                thread.start()  
                titulo = "Agregado Correctamente"
                mensaje = "Se ha registrado el producto correctamente"
                tema = "success"    
                
                return redirect('/listarEmpleados/')      
                                                                            
    except Error as e:
        transaction.rollback()
    
    
        
def generarPassword():
    longitud = 6
    
    caracteres = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    password = ''
    
    for i in range(longitud):
        password +=''.join(random.choice(caracteres))
    return password


def agregarServicio(request):
    try:
        estado = False
        mensaje = ''
        data = json.loads(request.body)
        nombre = data['nombre']
        tipo = data['tipo']
        precio = data['precio']
        descripcion = data['descripcion']
        idEm= data['empleado']
        with transaction.atomic():
            if idEm != '0':
                em = Empleado.objects.get(pk = idEm)
                servicio = Servicio(serNombre = nombre, serTipo = tipo, serEmpleado = em, serPrecio = precio, serDescripcion = descripcion)
                servicio.save()
                estado = True
                mensaje = 'Servicio Agregado Correctamente'
            else:
                servicio = Servicio(serNombre = nombre, serTipo = tipo, serPrecio = precio, serDescripcion = descripcion)
                servicio.save()
                estado = True
                mensaje = 'Servicio Agregado Correctamente'
            
    except Error as e:
        transaction.rollback()
        
    retorno = {'mensaje': mensaje, 'estado': estado}
    return JsonResponse(retorno)

def asignasServicio(request):
    try:
        try:
            estado = False
            mensaje = ''
            data = json.loads(request.body)
            servicio = data['servicio']
            empleado = data['empleado']
            with transaction.atomic():
                    si = Servicio.objects.get(pk = servicio)
                    em = Empleado.objects.get(pk = empleado)
                    si.serEmpleado = em
                    si.save()
                    estado = True
                    mensaje = 'Empleado Asignado Correctamente'
                    
        except ObjectDoesNotExist as e:
            transaction.rollback()
    except Exception as e:
        print(e)
        
    retorno = {'mensaje': mensaje, 'estado': estado}
    return JsonResponse(retorno)

def vistaAgregarCita(request, id,mensaje=""):
    ser = Servicio.objects.get(pk=id)
    if request.user.is_authenticated:
    # Código que se ejecuta si el usuario está autenticado y pertenece al grupo "Usuario"
        if request.user.groups.filter(name='Usuario'):
            usuario_actual = request.user
            mascotas_del_usuario = Mascota.objects.filter(masUser=usuario_actual)
            empleado_del_servicio = Empleado.objects.filter(servicio=ser)

            #Validamos que se agregue de la fecha actual en adelante
            fecha=datetime.now()
            fecha_actual=datetime.strftime(fecha,"%Y-%m-%d")
            
            # Obtenemos las horas ya reservadas para el servicio en la fecha actual
            horas_reservadas = Cita.objects.filter(ciFecha=fecha_actual, ciServicio=ser).values_list('ciHora', flat=True)

            # Definimos las horas de inicio y fin del horario de citas 
            hora_inicio = datetime.combine(datetime.today(), time(7, 0))  # 07:00 AM
            hora_fin = datetime.combine(datetime.today(), time(17, 0))    # 05:00 PM

            # Creamos una lista con todas las horas posibles en ese horario
            horas_posibles = [hora_inicio + timedelta(hours=i) for i in range((hora_fin.hour - hora_inicio.hour) + 1)]

            # Filtramos las horas que no están reservadas
            horas_no_reservadas = [hora for hora in horas_posibles if hora.strftime('%H:%M') not in horas_reservadas]
            
            retorno = {"ser": ser, "usuario": usuario_actual, "mascotas": mascotas_del_usuario, "empleado_del_servicio": empleado_del_servicio,"mensaje":mensaje,
                    "fecha_actual":fecha_actual, "horas_no_reservadas": horas_no_reservadas}
            
            return render(request, "CITAS.html", retorno)
        else: 
            return render(request, 'Error/403.html')
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        
        return redirect(f'/inicio/{mensaje}')
    
def agregarCita(request, id):
    if request.user.is_authenticated:
       
        idMascota = request.POST["txtNombreMasCita"]
        

        # Datos De la Cita ForeignKey
        fechaCita = request.POST["txtFechaCita"]
        horaCita = request.POST["txtHoraCita"]
        sintomasCita = request.POST["txtSintomasCita"]
        try:
            mascota = Mascota.objects.get(pk=idMascota)
            user = request.user
            servicio = Servicio.objects.get(pk=id)
            
            #Validamos que no se agreguen cita los sabados, los domingos 
            #No se repita la misma fecha con el mismo servicio
            fecha_datetime = datetime.strptime(fechaCita, "%Y-%m-%d")
            if fecha_datetime.weekday() in [5, 6]: # Sábado: 5, Domingo: 6
                mensaje = "No se pueden hacer reservas los sábados y domingos."
                ide = int(servicio.id)
                return redirect(f"/vistaAgregarCita/{ide}/{mensaje}/")
            # Consultar si no existe cita con el mismo veterinario y hora
            citas_exist = Cita.objects.filter(
                ciFecha=fechaCita, ciHora=horaCita, ciServicio=servicio
            ).exists()

            if citas_exist:
                mensaje ="Ya hay una cita reservada con el mismo veterinario y hora."
                ide = int(servicio.id)
                return redirect(f"/vistaAgregarCita/{ide}/{mensaje}/")
            else:
            # Crear el objeto Cita y asignar los valores
                cita = Cita(
                    ciMascota=mascota,
                    ciServicio=servicio,
                    ciUsuario=user,

                    ciFecha=fechaCita,
                    ciHora=horaCita,
                    ciSintomas=sintomasCita,
                    ciEstado='Solicitada'  # Aquí se proporcionar el estado de la cita que desees
                )
                cita.save()
                mensaje = "Cita agregada correctamente"
        except Exception as error:
                mensaje = f"Problemas al agregar la Cita. {error}"

        retorno = {"mensaje": mensaje, "cita": cita}
        return render(request, "perfilUsuario.html", retorno)

def cancelarCita(request, id):
    try:
        estado = False
        mensaje = ''
        ide = id
        with transaction.atomic():
            cita = Cita.objects.get(pk = ide)
            cita.ciEstado = 'Cancelada'
            cita.ciDescripcion = 'Cita fue cancenlada'
            cita.save()
            estado = True
            mensaje = "Cita Cancelada exitosamente"
    except Exception as error:
        transaction.rollback()
        print(error)
        mensaje = "ocurrio un error"
        retorno = {'estado': estado, 'mensaje': mensaje}
        return JsonResponse(retorno)
    
    retorno = {'estado': estado, 'mensaje': mensaje}
    return JsonResponse(retorno)
    

def citaRealizada(request, id): 
    try:
        estado = False
        mensaje = ''
        data = json.loads(request.body)
        descripcion = data['descripcion']
        with transaction.atomic():
            cita = Cita.objects.get(pk = id)
            cita.ciEstado = 'Atendida'
            cita.ciDescripcion = descripcion
            cita.save()
            estado = True
            mensaje = "Cita atentida correctamente, ya puedes generar el historial clinico!"
        
    except Exception as error:
        transaction.rollback()
        print(error)
    
    retorno = {'estado': estado, 'mensaje': mensaje}
    return JsonResponse(retorno)


##############################################################################
#Metodo De Compra
def finalizar_compra(request):
    if request.user.is_authenticated:
    # Obtener el carrito del usuario a través de la sesión
        if request.user.groups.filter(name='Usuario'):
            carrito = Carrito(request)

            # Obtener los datos del usuario logeado
            usuario = request.user  # Esto asume que has configurado la autenticación de usuario en tu proyecto

            # Obtener todos los productos en el carrito con sus detalles
            productos_en_carrito = []
            productos_distintos = set()  # Utilizamos un conjunto para almacenar los IDs de los productos distintos

            for key, value in carrito.carrito.items():
                producto_id = value["producto_id"]
                producto = Producto.objects.get(id=producto_id)
                detalle_producto = {
                    "producto": producto,
                    "cantidad": value["cantidad"],
                }
                productos_en_carrito.append(detalle_producto)


                productos_distintos.add(producto_id)  # Agregamos el ID del producto al conjunto

            cantidad_total_productos = len(productos_distintos)  # La cantidad de productos distintos es el tamaño del conjunto

            # Calcular el total del carrito después de la compra
            total = Carrito.total_carrito(request)

            # Pasar los datos a la plantilla HTML
            return render(request, 'procesoCompra.html', {'usuario': usuario, 'productos_en_carrito': productos_en_carrito, 'total': total, 'cantidad_total_productos': cantidad_total_productos})
        else: 
            return render(request, "Error/403.html")
    else:
        mensaje = "No has iniciado sesión"
        return redirect (f'/inicio/{mensaje}')
        
# Tu función para generar el código único numérico
def generar_codigo_unico_numerico(longitud=8):
    numeros = "0123456789"
    codigo = ''.join(random.choice(numeros) for _ in range(longitud))

    # Asegurarse de que el código generado sea único
    while Pedido.objects.filter(peCodigoPedido=codigo).exists():
        codigo = ''.join(random.choice(numeros) for _ in range(longitud))

    return codigo

# Tu función para procesar el pedido
def procesar_pedido(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                carrito = Carrito(request)
                # Obtener los datos del formulario
                nombre_completo = request.POST.get('txtNombreCompra')
                numero_identificacion = request.POST.get('txtNumeroIdentificacion')
                correo_electronico = request.POST.get('email')
                telefono = request.POST.get('txtTelefono')
                direccion = request.POST.get('txtDireccion')
                descripcion_direccion = request.POST.get('txtDireccionDes')
                departamento = request.POST.get('departamento')
                municipio = request.POST.get('municipio')
                metodo_pago = request.POST.get('state')
                total_carrito = carrito.total_carrito()
                total_pagar  = total_carrito
                # Datos de envío

                # Datos del pedido
                with transaction.atomic():
                    # Guardar en la base de datos
                    usuario = request.user
                    estado_pedido = 'Solicitado'
                    # Generar código único
                    codigoPedido = generar_codigo_unico_numerico()
                    total = int(total_pagar)
                    # Calcular el impuesto del 19%
                    impuesto_porcentaje = 19
                    impuesto = int(total * impuesto_porcentaje / 100)



                    # Crear objeto FormaDePago y guardar
                    metodo_pago = metodo_pago or "Sin especificar"
                    
                    # Creamo la descripcion del envio
                    descripcion_envio = f"Departemento: {departamento}, municipio: {municipio}, Direccion: {direccion}, Descripcion: {descripcion_direccion}"
                    # Crear objeto DetellaEnvio y guardar
                    envio = DetellaEnvio.objects.create(detNombreDestinatario = nombre_completo,
                                         detNitDestinatario = numero_identificacion,
                                         detDescripcion = descripcion_envio,
                                         detTelefonoDestinatario = telefono,
                                         detCorreoDestinatario = correo_electronico 
                                         )

                    # Crear objeto Pedido y guardar
                    pedido = Pedido(
                        peUsuario=usuario,
                        peEstado=estado_pedido,
                        peCodigoPedido= codigoPedido,
                        peImpuestoPedido=impuesto,
                        peTotalPedido=total_pagar,
                        peFormaPago=metodo_pago,
                        peDetEnvio=envio,
                    )
                    pedido.save()
                    
                    # Recorremos el objeto Carrito para hacer el detatllePedido
                    
                    for key, value in carrito.carrito.items():
                        producto_id = value["producto_id"]
                        producto = Producto.objects.get(pk = producto_id)
                        totalProductoCantidad = value["acumulado"]
                        cantida = value["cantidad"]
                        DetallePe =DetallePedido.objects.create(detCantida = cantida,  
                                                                detPrecio = totalProductoCantidad, 
                                                                detProducto = producto,
                                                                detPedido = pedido
                                                                )
                        DetallePe.save()
            except Exception as error:
                transaction.rollback()
                print(error)
            return redirect('/vistaPerfilusuario/')

def descargarPDFhistorial(request, id):
    try:
        ide = id
        citas = Cita.objects.get(pk=ide)
        archivo_path = generaPdfHistorial(citas)
        
        asunto = 'Registro Sistema Veterinaria Animalagro'
        mensaje = f'Cordial saludo, <b>{citas.ciUsuario.first_name} {citas.ciUsuario.last_name}</b>, nos permitimos,\
            informarle que la cita fue finalizada, y adjuntamos el historial clínico.\
            Esperamos tu pronto regreso.<br>'
        enviarCorreo(asunto, mensaje, citas.ciUsuario.email, archivo_path)
        
        retorno = {"estado": True, "mensaje": "PDF generado correctamente y enviado"}
        return JsonResponse(retorno)  # Si estás esperando una respuesta JSON
        
    except Exception as erro:
        print(erro)
        retorno = {"estado": False, "mensaje": "Error al generar o enviar el PDF"}
        return JsonResponse(retorno)  # Si estás esperando una respuesta JSON

def generaPdfHistorial(citas):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.mostrar(citas)
    # archivo = f'historial-{citas.ciFecha}-{citas.ciHora}.pdf'
    # archivo_path = os.path.join('media', archivo)
    # pdf.output(archivo_path, 'F')
    # return archivo_path
    fecha_hora_str = citas.ciFecha.strftime('%Y-%m-%d')
    hora = citas.ciHora.strftime('%H-%M-%S')
    archivo_nombre = f'historial-{fecha_hora_str}-{hora}.pdf'

    archivo_path = os.path.join('media', archivo_nombre)
    pdf.output(archivo_path, 'F')

    with open(archivo_path, 'rb') as pdf_file:
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{archivo_nombre}"'
    
    return archivo_path