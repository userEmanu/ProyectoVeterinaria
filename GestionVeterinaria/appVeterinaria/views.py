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
from django.http import JsonResponse
from appVeterinaria.carrito import *

# Aqui las vistas

def vistaInicio(request):
    # Obtener todos los objetos del modelo Servicio desde la base de datos
    servicio = Servicio.objects.all()

    # Crear un diccionario con la lista de objetos de Servicio y pasarlo a la plantilla
    retorno = {"servicio": servicio}
    return render(request, "index.html", retorno)

def vistaGestionCitas(request):
    retorno = {'cita': Cita.objects.all(), 'estado': estadoCita }   
    return render(request,"Administrador/frmGestionCitas.html", retorno)

def vistaCita(request):
    return render(request,"Administrador/frmCita.html")

def vistaCitas(request):
    if request.user.is_authenticated:
         return render(request, "CITAS.html")
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)

def vistaCodigo(request):
    return render(request, "codigoRecuperar.html")

def vistaGestionServicio(request):
    if request.user.is_authenticated:
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
        user= {"user": request.user,
                       "rol": request.user.groups.get().name, "servicio": Servicio.objects.all()}
        return render(request, "indexUsuario.html", user)
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)
    

def vistaPerfilUsuario(request,):
    if request.user.is_authenticated:
        user= {"user": request.user,
                       "rol": request.user.groups.get().name}
        return render(request, "perfilUsuario.html", user)
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)

def vistaRecuperarContra(request):
    return render(request, "RecuperarContraseña.html")

def vistaRegistrarse(request):
    retorno = {"identificacion": tipoDocumento}
    return render(request, "Registrarse.html", retorno)

def vistConNueva(request):
    return render(request, "DigitarContraseñaNueva.html")


def perfiladmin(request):
    return render(request, "Administrador/perfiladmin.html")

def VistaAgregarEmpleado(request):
    return render(request, "Administrador/frmagregarempleado.html")


# Aqui las vistas Gestion, son las que se cargan con datos o tienen Tablas 

def CerrarSesion(request):
    auth.logout(request)
    return redirect( "/inicio/",
                  {"mensaje":"Has cerrado la sesión"})


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
                if user.groups.filter(name='Administrador').exists():
                    return redirect('/vistaAdministrador')
                elif user.groups.filter(name='Asistente').exists():
                    return redirect('/inicio')
                else:
                    return redirect('/vistaIndexUsuario')
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
    return redirect("/VistaProductos/", retorno)

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
    try:
        empleado = Empleado.objects.get(pk = id)
        rol = Group.objects.all()
        retorno = {"empleado": empleado, "rol": rol, "tipo": tiposUsuarios}        
    except Error as e:
        print(e)    
        
    return render(request, "Administrador/registrarUsuarioEmpleado.html", retorno)

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
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)
    
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
        transaction.rollback()
        cita = Cita.objects.get(pk = id)
        cita.ciEstado = 'Cancelada'
        cita.save()
        estado = True
        mensaje = "Citas Cancelada exitosamente"
        
    except Exception as error:
        transaction.rollback()
        print(error)
    
    retorno = {'estado': estado, 'mensaje': mensaje}
    return JsonResponse(retorno)