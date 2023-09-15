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
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import Sum, Case, When, IntegerField
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
from django.http import JsonResponse
from fpdf import FPDF
from appVeterinaria.carrito import *
import pytz
from appVeterinaria.pdfHistorialClinico import PDF
from appVeterinaria.pdfPedidos import PDFPedido

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
        servicio = Servicio.objects.all()[:8]
        pro = Producto.objects.filter()[:4]
        # Crear un diccionario con la lista de objetos de Servicio y pasarlo a la plantilla
        retorno = {"servicio": servicio, "productos": pro, "mensaje": mensaje}
        return render(request, "index.html", retorno)

def vistaGestionCitas(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):
            return render(request, 'Error/403.html')
        else:
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total_pedidos_hoy = Pedido.objects.filter(peFecha = fecha_actual).count()
            ventashoy = {
                "countPedido": total_pedidos_hoy, "porcentaje": consultarPromedioDeVentasPorDia()
            }
            con = Contactanos.objects.all().count()
            rol = verificarRol(request)
            retorno = {'cita': Cita.objects.all(), 
                       'estado': estadoCita,
                       "rol": rol,
                       "ventashoy": ventashoy,
                       "contactanos": con,
                       "user": request.user}   
            return render(request,"Administrador/frmGestionCitas.html", retorno)
    else:
        return render(request, 'Error/403.html')
    
def vistaGestionPedidos(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):
            return render(request, 'Error/403.html')
        else:
            rol = verificarRol(request)
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total_pedidos_hoy = Pedido.objects.filter(peFecha = fecha_actual).count()
            ventashoy = {
                "countPedido": total_pedidos_hoy, "porcentaje": consultarPromedioDeVentasPorDia()
            }
            retorno = {
                "pedido": Pedido.objects.all().order_by('-peFecha'),
                "user": request.user,
                "estadoPedido": estadoPedido,
                "contactanos": Contactanos.objects.all().count(), 
                "rol": rol,
                "ventashoy": ventashoy
            }
            return render(request,"Administrador/frmGestionPedidos.html", retorno)
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
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total_pedidos_hoy = Pedido.objects.filter(peFecha = fecha_actual).count()
            ventashoy = {
                "countPedido": total_pedidos_hoy, "porcentaje": consultarPromedioDeVentasPorDia()
            }
            con = Contactanos.objects.all().count()
            rol = verificarRol(request)
            empleado = {'empleado': Empleado.objects.all(), 'servicio': Servicio.objects.all(),"user": request.user,
                        "roles": request.user.groups.get().name, 
                        "rol": rol,
                        "ventashoy": ventashoy,
                        "contactanos": con}
            return render(request, 'Administrador/frmGestionServicio.html', empleado)
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)


def verificarRol(request):
    if request.user.is_authenticated:
        rol = None
        if request.user.groups.filter(name='Administrador').exists():
            rol = 'Administrador'
        elif request.user.groups.filter(name='Asistente').exists():
            rol = 'Asistente'
        elif request.user.groups.filter(name='Medico').exists():
            rol = 'Medico'
        
        return rol
        
def vistaAdministrador(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):      
            return render(request, 'Error/403.html')
        else:
            
            rol = verificarRol(request)
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            
            total_pedidos_hoy = Pedido.objects.filter(peFecha = fecha_actual).count()
            ventashoy = {
                "countPedido": total_pedidos_hoy, "porcentaje": consultarPromedioDeVentasPorDia()
            }
            mesGancia, porcentaje = ventasYGananciasAumentaron()
            ingresosMes={
                "ingresosMes": mesGancia,
                "porcentaje": porcentaje
            }
            productos = productosMasVendidos()
            contactanos = Contactanos.objects.all().count()
            user= {"user": request.user,
                        "rol": request.user.groups.get().name, "ventashoy": ventashoy,
                        "ingresosEstemes": ingresosMes,  "productos": productos, "contactanos": contactanos, "rol": rol}
            return render(request, "Administrador/inicio.html",user)
    else:
        mensaje = "Debes Iniciar Sesión"
        titulo= "¿Iniciaste Sesión?"
        icon = "error"
        retorno = {"titulo": titulo, "mensaje": mensaje, "tema": icon}
        return render(request,"index.html", retorno)

def productosMasVendidos():
    productos_mas_vendidos = Producto.objects.annotate(
        cantidad_vendida=Coalesce(
            Sum(Case(When(detallepedido__detPedido__peEstado='Entregado', then='detallepedido__detCantida'), default=0, output_field=IntegerField())),
            0
        )
    ).order_by('-cantidad_vendida')[:5]

    return productos_mas_vendidos

def ventasYGananciasAumentaron():
    mes_actual = datetime.now().month
    año_actual = datetime.now().year

    # Consultar las ganancias del mes actual
    ganancias_mes_actual = Pedido.objects.filter(peFecha__year=año_actual, peFecha__month=mes_actual) \
                                        .aggregate(ganancias_mes=Sum('peTotalPedido'))['ganancias_mes']

    # Consultar las ganancias del mes anterior
    mes_anterior = mes_actual - 1 if mes_actual > 1 else 12
    año_anterior = año_actual if mes_actual > 1 else año_actual - 1
    ganancias_mes_anterior = Pedido.objects.filter(peFecha__year=año_anterior, peFecha__month=mes_anterior) \
                                           .aggregate(ganancias_mes=Sum('peTotalPedido'))['ganancias_mes']
    
    cambio_porcentual = 0  # Inicializar el cambio porcentual con 0
    ganacias = 0
    
    # Calcular el porcentaje de aumento o disminución
    if ganancias_mes_actual is not None and ganancias_mes_anterior is not None and ganancias_mes_anterior != 0:
        cambio_porcentual = ((ganancias_mes_actual - ganancias_mes_anterior) / ganancias_mes_anterior) * 100
        

    return ganancias_mes_actual, round(cambio_porcentual, 1)


    
def gananciasPorMes():
    año_actual = datetime.now().year
    # Consultar las ganancias por mes de los pedidos del año actual
    ganancias_por_mes = Pedido.objects.filter(peFecha__year=año_actual) \
                                    .values('peFecha__month') \
                                    .annotate(ganancias_mes=Sum('peTotalPedido')) \
                                    .order_by('peFecha__month')
    # Crear un diccionario para almacenar las ganancias por mes
    ganancias_mensuales = {mes['peFecha__month']: mes['ganancias_mes'] for mes in ganancias_por_mes}
    # Mostrar las ganancias por mes
    ganaciasPormes = []
    for mes_num in range(1, 13):
        ganancia = ganancias_mensuales.get(mes_num, 0)
        ganaciasPorMes ={
            "mes": mes_num,
            "ganancias": f"{ganancia:.2f}"
        }
        ganaciasPormes.append(ganaciasPorMes)
    
    return ganaciasPormes

        
        
def consultarPromedioDeVentasPorDia():
    fecha_actual = datetime.now().date()
    fecha_hace_una_semana = fecha_actual - timedelta(days=7)
    pedidos_por_dia = Pedido.objects.filter(peFecha__range=[fecha_hace_una_semana, fecha_actual]) \
                                    .values('peFecha') \
                                    .annotate(num_pedidos=Count('id')) \
                                    .order_by('peFecha')
    total_pedidos = sum(item['num_pedidos'] for item in pedidos_por_dia)
    dias = len(pedidos_por_dia)
    promedio_pedidos_por_dia = total_pedidos / dias
    pedidos_hoy = pedidos_por_dia[len(pedidos_por_dia) - 1]['num_pedidos']
    porcentaje_cambio = ((pedidos_hoy - promedio_pedidos_por_dia) / promedio_pedidos_por_dia) * 100
    porcentaje_cambio_redondeado = round(porcentaje_cambio, 1)
    return porcentaje_cambio_redondeado
    
    
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
            pedidos = Pedido.objects.filter(peUsuario = use).order_by('-peFecha')
            mas = Mascota.objects.filter(masUser = use)[:2]
            mascotas = Mascota.objects.filter(masUser = use)
            user= {"user": use,
                        "rol": request.user.groups.get().name, 
                        "pedido": pedidos, "mas": mas, 
                        "listaTipo": tipoDocumento,
                        "mascota": mascotas}
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
            rol = verificarRol(request)
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total_pedidos_hoy = Pedido.objects.filter(peFecha = fecha_actual).count()
            ventashoy = {
                "countPedido": total_pedidos_hoy, "porcentaje": consultarPromedioDeVentasPorDia()
            }
            retorno = {
                "contactanos": Contactanos.objects.all().count(),
                "user": request.user, 
                "rol": rol,
                "ventashoy": ventashoy
            }
            return render(request, "Administrador/perfiladmin.html", retorno)
    else:
        return render(request, 'Error/403.html')

def VistaAgregarEmpleado(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, 'Error/403.html')
        else:
            
            rol = verificarRol(request)
            empleados = Empleado.objects.all()
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total_pedidos_hoy = Pedido.objects.filter(peFecha = fecha_actual).count()
            ventashoy = {
                "countPedido": total_pedidos_hoy, "porcentaje": consultarPromedioDeVentasPorDia()
            }
            con = Contactanos.objects.all().count()
            retorno = {
                "user": request.user,
                "contactanos": Contactanos.objects.all().count(),
                "listarEmpleados":empleados, 
                "rol": rol,
                "ventashoy": ventashoy,
                "contactanos": con
            }
            return render(request, "Administrador/frmagregarempleado.html", retorno)
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


def verificarExitenciasDeUsuarios(email, doc= None):
    estado = False
    try:
            user = User.objects.get(username = email, email = email)
            estado = False
    except User.DoesNotExist:
        estado = True
        
    return estado
def registrarseUsuario(request):
    try: 
        estado = False
        mensajes = ""
        tipoDoc = request.POST.get('cbIdentificacioon')
        identificacion = request.POST.get('txtIdentificacion')
        telefono = request.POST.get('txtTelefono')
        nombre = request.POST.get('txtNombre')
        apellido = request.POST.get('txtApellido')
        email =  request.POST.get('txtCorreo')
        contraseña = request.POST.get('txtContraseña')
        
        verificar = verificarExitenciasDeUsuarios(email)
        if verificar == True:
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
        else: 
            mensajes = "Usuario ya existente"
            estado = False
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
            user = authenticate(username=usernamee, password=passworde, userEstado = "Activo")
            if user is not None:
                #registrar la variable de sesión
                auth.login(request, user)
                if user.groups.filter(name='Administrador').exists():
                    return redirect('/vistaAdministrador')
                elif user.groups.filter(name='Asistente').exists():
                    return redirect('/vistaAdministrador')
                elif user.groups.filter(name='Medico').exists():
                    return redirect('/vistaAdministrador')
                else:
                    return redirect('/vistaPerfilusuario')
            else:
                mensaje = "Credenciales Incorrectas, O Cuenta suspendida"
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
                    return redirect("/VistaAgregarEmpleado/")
                except Error as error:
                    mensaje=f"Problemas al agregar empleado. {error}"
                retorno = {"mensaje":mensaje, "empleado":empleado}
                return render(request,"Administrador/frmagregarempleado.html", retorno)
    else:
        return render(request, 'Error/403.html')




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
            return render(request, 'Error/403.html')
        else:
            proveedores = Proveedor.objects.all()
            categorias = Categoria.objects.all()
            es = estadoProducto
            rol = verificarRol(request)
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total_pedidos_hoy = Pedido.objects.filter(peFecha = fecha_actual).count()
            ventashoy = {
                "countPedido": total_pedidos_hoy, "porcentaje": consultarPromedioDeVentasPorDia()
            }
            retorno = {"proveedores": proveedores, 
                       "categorias": categorias,
                       "estados": es, 
                       "user": request.user,
                       "rol": rol,
                       "contactanos": Contactanos.objects.all().count(),
                       "ventashoy": ventashoy}
           
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
        em= None
        with transaction.atomic():
            em = Empleado.objects.get(pk = id)
            if em != None:  
                verificar = verificarExitenciasDeUsuarios(em.emCorreo)      
                if verificar == True:        
                    user = User.objects.create(userTipoDoc = em.emTipoDoc,  userNoDoc = em.emNumeroDoc, userTelefono = em.emTelefono,
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
                    
                    return redirect('/VistaAgregarEmpleado/')      
                else:
                    user = User.objects.get(username = em.emCorreo, email = em.emCorreo)
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
                    
                    return redirect('/VistaAgregarEmpleado/')
                    
                                                                           
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
        return redirect('/vistaPerfilusuario/')

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
                    
                    fecha = datetime.now()
                    fecha_actual = datetime.strftime(fecha, "%Y-%m-%d")
                    colombia_timezone = pytz.timezone('America/Bogota')
                    # Obtener la hora actual en Colombia
                    hora_colombiana = datetime.now(colombia_timezone).strftime("%H:%M:%S")
                    pedido = Pedido.objects.create(
                        peUsuario=usuario,
                        peEstado=estado_pedido,
                        peCodigoPedido= codigoPedido,
                        peImpuestoPedido=impuesto,
                        peTotalPedido=total_pagar,
                        peFormaPago=metodo_pago,
                        peFecha = fecha_actual,
                        peHora = hora_colombiana,
                        peDetEnvio = envio
                    )
                    pedido.save()
                    
                    
                    detallePdf = []
                    # Recorremos el objeto Carrito para hacer el detatllePedido
                    
                    for key, value in carrito.carrito.items():
                        producto_id = value["producto_id"]
                        producto = Producto.objects.get(pk = producto_id)
                        totalProductoCantidad = value["acumulado"]
                        cantida = value["cantidad"]
                        detallePdf.append([str(producto.proNombre), cantida, str(producto.proPrecio), totalProductoCantidad])
                        DetallePe =DetallePedido.objects.create(detCantida = cantida,  
                                                                detPrecio = totalProductoCantidad, 
                                                                detProducto = producto,
                                                                detPedido = pedido
                                                                )
                        DetallePe.save()
                        
                    tabla = "<table class='table table-bordered text-center fw-bold' border='1'><thead><tr><th>Nombre Producto</th><th>Cantidad</th><th>Precio Unidad</th><th>Precio Total</th></tr></thead><tbody>"
            
                    for det in detallePdf:
                        tabla += f"""<tr>
                                        <td> {det[0]}</td>
                                        <td> {det[1]} </td>
                                        <td> {det[2]} </td>
                                        <td> {det[3]} </td>
                                    </tr>"""
                                        
                    tabla += "</tbody></table>"
                    
                    archivo = generaPdfPedido(codigoPedido, direccion)
                    asunto='Sistema Veterinaria Animalagro'
                    mensaje=f'Cordial saludo, <b>{usuario.first_name} {usuario.last_name}</b>, nos permitimos,\
                        informarle que usted ha hecho un pedido, con el codigo: {codigoPedido}, que se ah registrado de forma\
                        exitosa, recuerda hacer el proceso de pago, en el pdf estan lo metodos de pago de acuerdo a la forma que hayas elegido, puedes pagar.\
                        Recuerda subir una imagen del comprobante de pago en la plataforma, correo, o whatsapp.<br>\
                        <br>\
                        <b>Detalle del pedido</b><br> \
                        {tabla}'
                        
                    thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, usuario.email, archivo))
                    thread.start()
                    
                    return redirect('/vistaPerfilusuario/')
                
            except Exception as error:
                transaction.rollback()
                print(error)
            return redirect('/vistaIndexUsuario/')

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
    fecha_hora_str = citas.ciFecha.strftime('%Y-%m-%d')
    hora = citas.ciHora.strftime('%H-%M-%S')
    archivo_nombre = f'historial-{fecha_hora_str}-{hora}.pdf'

    archivo_path = os.path.join('media', archivo_nombre)
    pdf.output(archivo_path, 'F')

    with open(archivo_path, 'rb') as pdf_file:
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{archivo_nombre}"'
    
    return archivo_path


def generaPdfPedido(codigo, di):
    pe =  Pedido.objects.get(peCodigoPedido = codigo)
    det = DetallePedido.objects.filter(detPedido = pe)
    pdf = PDFPedido()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.mostrar(det, pe, di)
    archivo_nombre = f'pedido-{pe.peCodigoPedido}.pdf'

    archivo_path = os.path.join('media', archivo_nombre)
    pdf.output(archivo_path, 'F')

    with open(archivo_path, 'rb') as pdf_file:
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{archivo_nombre}"'
    
    return archivo_path


def detallePedido(request, id):
    try:
        ide = id
        ped = Pedido.objects.get(pk=ide)
        detalles = DetallePedido.objects.filter(detPedido=ped)
        lista_detalles = []  
        for det in detalles:
            detalle = {
                "Nombre": det.detProducto.proNombre,
                "precioUni": det.detProducto.proPrecio,
                "cantidad": det.detCantida,
                "precio": det.detPrecio
            }
            lista_detalles.append(detalle)  
        pedido = {
            "idPedido": ped.pk,
            "foto": str(ped.proFotoComprobante),
            "estado": ped.peEstado
        }
    
        retorno = {"detalle": lista_detalles, "estado": True, "ped": pedido, "estado": estadoPedido}
        return JsonResponse(retorno)
    except Exception as er:
        print("Error")



def cargarImagenComprobantePedido(request, id):
    try:
        ide = id
        estado = True
        file = request.FILES.get('fileFoto')
        with transaction.atomic():
            pedido = Pedido.objects.get(pk=ide)
            pedido.proFotoComprobante = file
            pedido.peEstado = 'Pago Cargado'
            pedido.save()
            retorno = {
                "mensaje": "Foto cargada correctamente, pronto tu pedido llegara a tu casa, debes estar pendiente a tu correo!",
                "estado": True
            }
            return JsonResponse(retorno)
    except Exception as ero:
        transaction.rollback()
        print(str(ero))

def AgregarMascota(request):
    try:
        # Obtener los datos del formulario
        estado = True
        Mensaje = ""
        nombreM = request.POST['nombreMas']
        fotoM = request.FILES.get('editFotoInput')
        razaM = request.POST['razaMas']
        tipoM = request.POST['tipoMas']
        if nombreM != "" and fotoM != "" and razaM != "" and tipoM != "":

            usuario_actual = request.user

            # Crear una nueva instancia del modelo Mascota con los datos recibidos y el usuario actual
            nueva_mascota = Mascota.objects.create(masNombre=nombreM, masFoto=fotoM, masRaza=razaM, masTipoAnimal=tipoM, masUser=usuario_actual)
            nueva_mascota.save()  # Guardar la mascota en la base de datos
            Mensaje = "Mascota agregada correctamente"
            estado = True
            retorno = {
                "mensaje": Mensaje, "estado": estado
            }
            return JsonResponse(retorno)
        else:
            Mensaje = "Faltan Datos"
            estado = False
            retorno = {
                "mensaje": Mensaje, "estado": estado
            }
            return JsonResponse(retorno)
    except Exception as e:
        print(e)

def cambiarestadoPedido(request, id):
    try:
        estado = False
        mensaje = ''
        ide = id
        data = json.loads(request.body)
        estado = data["estado"]
        with transaction.atomic():
            pedido = Pedido.objects.get(pk = ide)
            pedido.peEstado = estado
            pedido.save()
            
            estado = True
            mensaje = "Estado del pedido cambiado correctamente"
            retorno = {
                "estado": estado, "mensaje": mensaje
            }
            return JsonResponse(retorno)
    except Exception as er:
        transaction.rollback()
        print(er)
        
def subirImagenPerfilUser(request, id):
    try:
        estado = False
        mensaje = ""
        user =User.objects.get(pk = id)
        file = request.FILES.get('FilefotoPerfil')
        if file != False:
            user.userFoto = file
            user.save()
            estado = True
            mensaje = "Foto actualizada correctamente"
            retorno = {
                "estado": estado, "mensaje": mensaje
            }
            return JsonResponse(retorno)
        else:
            mensaje = "Elige una foto"
            estado = False
            retorno = {
                "estado": estado, "mensaje": mensaje
            }
            return JsonResponse(retorno)
        
    except Exception as er:
        print(er)
        
def actualizarDatosUsuario(request, id): 
    try:
        estado = False
        mensaje = ""
        nombre = request.POST["nombreEdit"]
        apellido = request.POST["apellidoEdit"]
        correo = request.POST["emailEdit"]
        telefono = request.POST["telefonoEdit"]
        numeroDoc = request.POST["noDocEdit"]
        tipodoc = request.POST["cbTipoEdit"]
        
        with transaction.atomic():
            user = User.objects.get(pk = id)
            user.first_name = nombre
            user.last_name = apellido
            user.email = correo
            user.userTelefono = telefono
            user.userNoDoc = numeroDoc
            user.userTipoDoc = tipodoc
            user.save()
            estado = True
            mensaje = "Informacion Actualizada Correctamente"
            
            retorno = {
                "mensaje": mensaje , "estado": estado
            }
            return JsonResponse(retorno)
    except ExceptionGroup as erro:
        transaction.rollback()
        print(erro)

def cancelarPedidoUser(request, id):
    try:
        ide = id
        estado = False
        with transaction.atomic():
            pedido = Pedido.objects.get(pk = ide)
            pedido.peEstado = "Cancelado"
            pedido.save()
            estado = True
            mensaje = "Pedido cancelado"
            retorno = {
                "estado": estado, "mensaje": mensaje
            }
            return JsonResponse(retorno)
            
    except Exception as er:
        transaction.rollback()
        print(er)
        
def vistasListarUsuarios(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):    
            return render(request, 'Error/403.html')
        else:
            
            rol = verificarRol(request)
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            total_pedidos_hoy = Pedido.objects.filter(peFecha = fecha_actual).count()
            ventashoy = {
                "countPedido": total_pedidos_hoy, "porcentaje": consultarPromedioDeVentasPorDia()
            }
            empleados = Empleado.objects.all() 
            empleados = Empleado.objects.all() 
            retorno = []
            for em in empleados: 
                usuariosEm = User.objects.filter(userEmpleado=em)
                for usuario in usuariosEm:
                    li = {
                        "first_name": usuario.first_name,
                        "last_name": usuario.last_name,
                        "username": usuario.username,
                        "email": usuario.email,
                        "userEstado": usuario.userEstado,  
                        "empleado": {
                            "emNombre": usuario.userEmpleado.emNombre,  
                            "emApellido": usuario.userEmpleado.emApellido,  
                        },
                    }
                    retorno.append(li)

            cuerpo = {
                "contactanos": Contactanos.objects.all().count(),
                "user": request.user, 
                "rol": rol,
                "ventashoy": ventashoy,
                "empleados_info": retorno
            }

            return render(request, "Administrador/listarUsuarios.html", cuerpo)

    else:
        return render(request, 'Error/403.html')