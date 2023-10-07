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
import re
from django.db.models.functions import Coalesce
from django.db.models import Sum, Case, When, IntegerField, F
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
from django.views.generic import TemplateView
from django.db.models import Q

# Aqui las vistas

def vistaNosotrosInformacion(request):
    return render(request, 'Nosotros.html')

def vistaServiciosTienda(request):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
        carrito = Carrito(request)
        total = carrito.total_carrito()
        categorias = Categoria.objects.all()[:7]
        proveedores = Proveedor.objects.all()[:6]
        servicios = Servicio.objects.all()[:5]
        ser = Servicio.objects.filter(serEstado = "Disponible")
        return render(request, "serviciosTienda.html", {'serviciosMostrar':ser, 'total': total,
                                                'categoria': categorias, 
                                               'proveedores': proveedores, 
                                               'servicios': servicios})
def vistaServiciosTiendaDescripcion(request, id):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
        idDelServicio = id
        carrito = Carrito(request)
        total = carrito.total_carrito()
        categorias = Categoria.objects.all()[:7]
        proveedores = Proveedor.objects.all()[:6]
        servicios = Servicio.objects.all()[:5]
        ser = Servicio.objects.get(pk = idDelServicio)
        return render(request, "detalleDelServicio.html", {'ser':ser, 'total': total,
                                                'categoria': categorias, 
                                               'proveedores': proveedores, 
                                               'servicios': servicios})
def vistaTienda(request):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
            productos = Producto.objects.filter(proEstado__in = ("Disponible", "Promocion"))
            carrito = Carrito(request)
            total = carrito.total_carrito()
            categorias = Categoria.objects.all()[:7]
            proveedores = Proveedor.objects.all()[:6]
            servicios = Servicio.objects.all()[:6]
            return render(request, "tienda.html", {'productos':productos, 'total': total,
                                                'categoria': categorias, 
                                               'proveedores': proveedores, 
                                               'servicios': servicios})
            
def vistaTiendaCategoria(request, id):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
        idCat = id
        cat = Categoria.objects.get(pk = idCat)
        productos = Producto.objects.filter(proCategoria = cat, proEstado__in = ("Disponible", "Promocion"))
        carrito = Carrito(request)
        total = carrito.total_carrito()
        categorias = Categoria.objects.all()[:7]
        proveedores = Proveedor.objects.all()[:6]
        servicios = Servicio.objects.all()[:6]
        return render(request, "tienda.html", {'productos':productos, 'total': total, 
                                            'categoria': categorias, 'proveedores': proveedores, 'servicios': servicios})
        
        
def vistaTiendaMarcas(request, id):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
        idMarcar = id
        prove = Proveedor.objects.get(pk = idMarcar)
        productos = Producto.objects.filter(proProveedor = prove, proEstado__in = ("Disponible", "Promocion"))
        carrito = Carrito(request)
        total = carrito.total_carrito()
        categorias = Categoria.objects.all()[:7]
        proveedores = Proveedor.objects.all()[:6]
        servicios = Servicio.objects.all()[:6]
        return render(request, "tienda.html", {'productos':productos, 'total': total, 
                                            'categoria': categorias, 'proveedores': proveedores, 'servicios': servicios})
        
        
def vistaTiendaPromociones(request):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
        productos = Producto.objects.filter(proEstado= "Promocion")
        carrito = Carrito(request)
        total = carrito.total_carrito()
        categorias = Categoria.objects.all()[:7]
        proveedores = Proveedor.objects.all()[:6]
        servicios = Servicio.objects.all()[:6]
        return render(request, "tienda.html", {'productos':productos, 'total': total,
                                            'categoria': categorias, 
                                            'proveedores': proveedores, 
                                            'servicios': servicios})

def vistaCarrito(request):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
        categorias = Categoria.objects.all()[:7]
        proveedores = Proveedor.objects.all()[:6]
        servicios = Servicio.objects.all()[:6]
        carrito = Carrito(request)
        total = carrito.total_carrito()
        retorno = {'total': total, 'categoria': categorias, 
                                                'proveedores': proveedores, 
                                                'servicios': servicios}
        return render(request, "carrito.html", retorno)

def vistaDetalleProducto(request,id):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
        producto = Producto.objects.get(pk=id)
        productos = Producto.objects.filter(proEstado__in = ("Disponible", "Promocion"))[:8]
        carrito = Carrito(request)
        total = carrito.total_carrito()  
        categorias = Categoria.objects.all()[:7]
        proveedores = Proveedor.objects.all()[:6]
        servicios = Servicio.objects.all()[:6]  
        return render(request, 'detalleProducto.html', {'producto': producto, 
                                                        'productos': productos, 
                                                        'total': total,
                                                        'categoria': categorias, 
                                                        'proveedores': proveedores, 
                                                        'servicios': servicios})


def buscar_productos(request):
    if request.user.is_authenticated and request.user.groups.filter(name__in=('Administrador', 'Asistente', 'Medico')):
            return redirect('/vistaAdministrador/')
    else:
        consulta = request.GET.get('txtNombre')
        resultados = Producto.objects.filter(Q(proNombre__icontains=consulta) | Q(proNombre__icontains=consulta.lower()) | Q(proNombre__icontains=consulta.upper()), proEstado__in = ("Disponible", "Promocion"))
        carrito = Carrito(request)
        categorias = Categoria.objects.all()[:7]
        proveedores = Proveedor.objects.all()[:6]
        servicios = Servicio.objects.all()[:6]
        total = carrito.total_carrito()
        return render(request, 'buscarProducto.html', {'resultados': resultados, 
                                                    'consulta': consulta , 
                                                    'total': total,
                                                        'categoria': categorias, 
                                                        'proveedores': proveedores, 
                                                        'servicios': servicios})

def eliminar_producto_carrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.eliminar(producto)
    return redirect("tienda")

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
        pro = Producto.objects.filter(proEstado__in = ("Disponible", "Promocion"))[:4]
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
                "pedidoPorEntregar": Pedido.objects.filter(peEstado__in=('Pago Cargado', 'Enviado')),
                "pedidoSolicitado": Pedido.objects.filter(peEstado = "Solicitado"),
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
            servicioDirigianimales = servicioDirigido_animales
            rol = verificarRol(request)
            empleado = {'empleado': Empleado.objects.all(), 'servicio': Servicio.objects.all(),"user": request.user,
                        "roles": request.user.groups.get().name, 
                        "rol": rol,
                        "ventashoy": ventashoy,
                        "contactanos": con,
                        "animalDirigido": servicioDirigianimales}
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

def clientesEnElaño():
    año_actual = datetime.now().year #Se saca el año actua

    # Realizamos una consulta donde tomamos todos lo meses del año y la comparamos con el actual
    cantidad_De_Usuarios = User.objects.filter(
        pedido__peFecha__year=año_actual
    ).annotate(num_pedidos=Count('pedido')).filter(num_pedidos__gt=0).count() 
    
    # retornamos la cantidad de clientes que han comprado en el año
    return cantidad_De_Usuarios 

def consultarClienteQmasCompra():
    usuarios_mas_compradores = User.objects.annotate(total_compras=Count('pedido')).order_by('-total_compras')[:5]

    resultados_json = []

    for usuario in usuarios_mas_compradores:
        productos_mas_comprados_usuario = DetallePedido.objects.filter(detPedido__peUsuario=usuario, detPedido__peEstado = "Entregado") \
            .values('detProducto__proNombre', 'detProducto__proEstado') \
            .annotate(cantidad_total_comprada=Sum('detCantida'), 
                      precio_total=Sum(F('detCantida') * F('detPrecio'))) \
            .order_by('-cantidad_total_comprada') \
            .first()

        if productos_mas_comprados_usuario:
            user_nombre = usuario.username
            pro_nombre = productos_mas_comprados_usuario['detProducto__proNombre']
            pro_estado = productos_mas_comprados_usuario['detProducto__proEstado']
            cantidad_total_comprada = productos_mas_comprados_usuario['cantidad_total_comprada']
            precio_total = productos_mas_comprados_usuario['precio_total']

            resultado = {
                "userNombre": user_nombre,
                "proNombre": pro_nombre,
                "proPrecio": precio_total,  
                "proCantidad": cantidad_total_comprada,  
                "proEstado": pro_estado
            }

            resultados_json.append(resultado)

    return resultados_json


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
            clientes = clientesEnElaño()
            productos = productosMasVendidos()
            clientesMasCompradoresLista = consultarClienteQmasCompra()
            contactanos = Contactanos.objects.all().count()
            user= {"user": request.user,
                        "rol": request.user.groups.get().name, "ventashoy": ventashoy,
                        "ingresosEstemes": ingresosMes, 
                        "productos": productos,
                        "contactanos": contactanos, 
                        "rol": rol,
                        "clientesAnual": clientes,
                        "clientes": clientesMasCompradoresLista}
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
    ganancias_mes_actual = Pedido.objects.filter(peFecha__year=año_actual, peFecha__month=mes_actual, peEstado="Entregado") \
                                        .aggregate(ganancias_mes=Sum('peTotalPedido'))['ganancias_mes']

    # Consultar las ganancias del mes anterior
    mes_anterior = mes_actual - 1 if mes_actual > 1 else 12
    año_anterior = año_actual if mes_actual > 1 else año_actual - 1
    ganancias_mes_anterior = Pedido.objects.filter(peFecha__year=año_anterior, peFecha__month=mes_anterior, peEstado="Entregado") \
                                           .aggregate(ganancias_mes=Sum('peTotalPedido'))['ganancias_mes']
    
    cambio_porcentual = 0  # Inicializar el cambio porcentual con 0
    ganacias = 0
    
    # Calcular el porcentaje de aumento o disminución
    if ganancias_mes_actual is not None and ganancias_mes_anterior is not None and ganancias_mes_anterior != 0:
        cambio_porcentual = ((ganancias_mes_actual - ganancias_mes_anterior) / ganancias_mes_anterior) * 100
        

    return ganancias_mes_actual, round(cambio_porcentual, 1)


    
def gananciasPorMes():
    año_actual = datetime.now().year
    
    ganancias_por_mes = Pedido.objects.filter(peFecha__year=año_actual) \
                                    .values('peFecha__month') \
                                    .annotate(ganancias_mes=Sum('peTotalPedido')) \
                                    .order_by('peFecha__month')
    ganancias_mensuales = {mes['peFecha__month']: mes['ganancias_mes'] for mes in ganancias_por_mes}
    ganaciasPormes = []
    for mes_num in range(1, 13):
        ganancia = ganancias_mensuales.get(mes_num, 0)
        ganaciasPorMes ={
            "mes": mes_num,
            "ganancias": f"{ganancia:.2f}"
        }
        ganaciasPormes.append(ganaciasPorMes)
    
    return ganaciasPormes


def datosBimestralesAnuales(request):
    hoy = datetime.now()
   

    resultados = []
    ganancias_mes_anterior = 0
    

    for mes_inicio in range(1, 13, 2):
        mes_fin = mes_inicio + 1 if mes_inicio + 1 <= 12 else 1
        inicio_bimestre = datetime(hoy.year, mes_inicio, 1)
        fin_bimestre = datetime(hoy.year, mes_fin, 1) - timedelta(days=1)

        
        ganancias_bimestre = Pedido.objects.filter(
            peFecha__range=[inicio_bimestre, fin_bimestre],
            peEstado="Entregado"  
        ).aggregate(ganancias_bimestre=Sum('peTotalPedido'))['ganancias_bimestre'] or 0

        total_pedidos_bimestre = Pedido.objects.filter(
            peFecha__range=[inicio_bimestre, fin_bimestre],
            peEstado="Entregado"  
        ).count()

        clientes_bimestre = Pedido.objects.filter(
            peFecha__range=[inicio_bimestre, fin_bimestre],
            peEstado="Entregado" 
        ).values('peUsuario').distinct().count()

        porcentaje_crecimiento = 0
        if ganancias_mes_anterior > 0 and ganancias_bimestre > 0:
            porcentaje_crecimiento = ((ganancias_bimestre - ganancias_mes_anterior) / ganancias_mes_anterior) * 100

        if mes_fin == 1:
            nombre_bimestre = f"{inicio_bimestre.strftime('%B')} - {datetime(hoy.year, 12, 1).strftime('%B')}"
        else:
            nombre_bimestre = f"{inicio_bimestre.strftime('%B')} - {datetime(hoy.year, mes_fin, 1).strftime('%B')}"
        if porcentaje_crecimiento < 0: 
            porcentaje_crecimiento = 0
        resultados.append({
            "nombre_bimestre": nombre_bimestre,
            "ventas": ganancias_bimestre,
            "total_pedidos": total_pedidos_bimestre,
            "clientes": clientes_bimestre,
            "porcentaje_crecimiento": round(porcentaje_crecimiento, 1)
        })

        ganancias_mes_anterior = ganancias_bimestre
        total_pedidos_mes_anterior = total_pedidos_bimestre

    return JsonResponse({"resultados": resultados})
        
 
def consultarPromedioDeVentasPorDia():
    fecha_actual = datetime.now().date()
    fecha_hace_una_semana = fecha_actual - timedelta(days=7)
    pedidos_por_dia = Pedido.objects.filter(peFecha__range=[fecha_hace_una_semana, fecha_actual]) \
                                    .values('peFecha') \
                                    .annotate(num_pedidos=Count('id')) \
                                    .order_by('peFecha')
    total_pedidos = sum(item['num_pedidos'] for item in pedidos_por_dia)
    dias = len(pedidos_por_dia)
    if total_pedidos != 0:
        promedio_pedidos_por_dia = total_pedidos / dias
        pedidos_hoy = pedidos_por_dia[len(pedidos_por_dia) - 1]['num_pedidos']
        porcentaje_cambio = ((pedidos_hoy - promedio_pedidos_por_dia) / promedio_pedidos_por_dia) * 100
        porcentaje_cambio_redondeado = round(porcentaje_cambio, 1)
    else: 
        porcentaje_cambio_redondeado = 0
    return porcentaje_cambio_redondeado
    
    
def vistaUsuario(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuario'):      
            user= {"user": request.user,
                       "rol": request.user.groups.get().name, 
                       "servicio": Servicio.objects.all(),
                       "productos": Producto.objects.all()[:4]}
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

def error_404(request, exception):
   context = {}
   return render(request,'Error/404.html', context)
# def error404(request, exception):
#     return render(request, 'Error/403.html', status=404)

def CerrarSesion(request):
    auth.logout(request)
    mensaje = "Sesión Cerrada Con Exito"
    return redirect( f"/inicio/{mensaje}")


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

def enviarCorreoDosDestinatarios(asunto=None, mensaje=None, destinatarios=None, archivo=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'destinatarios': destinatarios, 
        'mensaje': mensaje,
        'asunto': asunto,
        'remitente': remitente,
    })
    
    try:
        correo = EmailMultiAlternatives(
            asunto, mensaje, remitente, destinatarios)
        correo.attach_alternative(contenido, 'text/html')
        if archivo is not None:
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

def VerificarCOntraseña(con):
    estado = False
    patron = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=])'
    estado = bool(re.match(patron, con))
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
        if tipoDoc != "" and identificacion != "" and telefono != "" and nombre != "" and apellido != "" and email != "" and contraseña != "":
            estadoCOntra = VerificarCOntraseña(contraseña)
            if estadoCOntra == True:
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
                        estado = True
                        mensajes = "Registro Exitoso, Ya Puedes Iniciar Sesión"
                        
                        asunto='Registro Sistema Veterinaria Animalagro'
                        mensaje=f'Cordial saludo, <b>{usuario.first_name} {usuario.last_name}</b>, nos permitimos,\
                            informarle que usted ha sido registrado en el Sistema de nuestra veterinaria Animalagro \
                            ubicada en campoalegre, Huila, ubicada Ca 12 calle 18.\
                            Nos permitimos enviarle las credenciales de Ingreso a nuestro sistema.<br>\
                            <br><b>Username: </b> {usuario.username}\
                            <br><b>Password: </b> {contraseña}'
                        thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, usuario.email) )
                        thread.start()
                        
                        retorno = {"mensaje": mensajes, "estado": estado}
                        return JsonResponse(retorno)
                        
                else: 
                    mensajes = "Este correo electrónico ya ha sido utilizado para crear una cuenta. ¿Quieres iniciar sesión en lugar de registrarte de nuevo?"
                    estado = False
                    retorno = {"mensaje": mensajes, "estado": estado} 
                    return JsonResponse(retorno)
            else:
                restorno = {
                "estado": False, 
                "mensaje": "La contraseña Debe tener, mayusculas, minusculas, numeros y caracteres"
                }
                return JsonResponse(restorno)
        else:
            restorno = {
                "estado": False, 
                "mensaje": "Faltan Datos"
            }
            return JsonResponse(restorno)
    except Error as error:
        transaction.rollback()
        print(error)
     



def IniciarSesion(request):
    try:
        with transaction.atomic():
            usernamee= request.POST["txtUsuario"] 
            passworde = request.POST["txtContraseña"]
            estado = "Activo"
            user = authenticate(username=usernamee, password=passworde)
            if user is not None:
                #registrar la variable de sesión
                if user.userEstado == estado:
                    
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
                   mensaje = "Cuenta suspendida"
                   return redirect(f'/inicio/{mensaje}') 
            else:
                mensaje = "Credenciales Incorrectas"
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
        colombia_timezone = pytz.timezone('America/Bogota')
        now_colombia = timezone.now().astimezone(colombia_timezone)
        contac = Contactanos(conNombre = nombreCon, conEmail = emailCon, conNumeroTe = numeroCon,
                           conMensaje =mensajeCon, conFecha =now_colombia.strftime("%Y-%m-%d") , conHora = now_colombia.strftime("%H:%M"))
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
            
            producto = Producto.objects.all()
            retorno = {"proveedores": proveedores, 
                       "categorias": categorias,
                       "estados": es, 
                       "user": request.user,
                       "rol": rol,
                       "contactanos": Contactanos.objects.all().count(),
                       "ventashoy": ventashoy,
                       "listarProductos":producto}
           
            return render(request, "Administrador/frmAgregarProveedor.html", retorno)
    else:
        return render(request, 'Error/403.html')

def eliminar_product(request, id): 
    producto = get_object_or_404(Producto, pk=id)

    if request.method == 'POST':
        producto.proEstado = "Eliminado"
        producto.save()
        return redirect('/VistaProductos/')



def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST['editNombre']
        estado = request.POST['editEstado']
        precio = request.POST['editPrecio']
        descripcion = request.POST['editDescripcion']
        descuento = request.POST['editDescuento']
        # Actualizar los campos del producto
        producto.proNombre = nombre
        producto.proEstado = estado
        producto.proPrecio = precio
        producto.proDescripcion = descripcion
        producto.proDescuento = descuento

        # Obtener la imagen nueva del formulario
        if 'editFoto' in request.FILES:
            imagen_nueva = request.FILES['editFoto']
            producto.proFoto = imagen_nueva

        # Guardar el producto actualizado en la base de datos
        producto.save()

        # Redireccionar a la lista de productos
        return redirect('/VistaProductos/')  # Ajusta la URL según tu configuración

    return redirect("/VistaProductos/")


def RegistrarProducto(request):
    if request.method == 'POST':
        estado = False
        try:
            with transaction.atomic():
                # Traemos los datos del formulario de productos
                nombre_producto = request.POST.get("txtNombreP")
                estado_pro = request.POST.get("cbEstado")
                precio_producto = int(request.POST.get("txtPrecioP"))
                descuento = int(request.POST.get("txtDescuentoP"))
                archivo = request.FILES.get("fileFoto")
                descripcion_producto = request.POST.get("txtDescripcionP")
                id_proveedor = int(request.POST.get('cbProvedor'))
                id_categoria = int(request.POST.get('cbCategoria'))
                cat_recibe = Categoria.objects.get(pk=id_categoria)
                pro_recibe = Proveedor.objects.get(pk=id_proveedor)

                # Creamos un producto
                producto = Producto.objects.create(
                    proNombre=nombre_producto,
                    proEstado=estado_pro,
                    proPrecio=precio_producto,
                    proDescripcion=descripcion_producto,
                    proFoto=archivo,
                    proProveedor=pro_recibe,
                    proCategoria=cat_recibe,    
                )
                if descuento != "":
                    producto.proDescuento = descuento
                else:
                    producto.proDescuento = 0
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



def agregar_producto(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.agregar(producto)
    # return redirect("tienda")
    return JsonResponse({"estado": True})

def eliminar_producto(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.eliminar(producto)
    return JsonResponse({"estado": True})

def restar_producto(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.restar(producto)
    return JsonResponse({"estado": True})

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("tienda")

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
            em.emUsuario= "Creado"
            em.save()
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
        nombre = request.POST["txtNombreServicio"]
        tipo = request.POST["txtTiposer"]
        precio = request.POST["txtPrecioSer"]
        descripcion = request.POST["txtDescripcionser"]
        fotoSer = request.FILES.get("fileFotoSer")
        idEm= request.POST["cbEmpleado"]
        animalDirigido = request.POST["cbTipoAnimalDirigido"]
        with transaction.atomic():
            if idEm != '0':
                em = Empleado.objects.get(pk = idEm)
                servicio = Servicio(serNombre = nombre, serTipo = tipo, serEmpleado = em,
                                    serPrecio = precio, 
                                    serDescripcion = descripcion, serFoto =fotoSer, serDirigido = animalDirigido)
                servicio.save()
                estado = True
                mensaje = 'Servicio Agregado Correctamente'
            else:
                servicio = Servicio(serNombre = nombre, serTipo = tipo, serPrecio = precio, serDescripcion = descripcion, serFoto =fotoSer, serDirigido = animalDirigido)
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
        servicio = Servicio.objects.get(pk=id)
        if servicio.serDirigido == "Animales Domesticos":
            idMascota = request.POST["txtNombreMasCita"]
        fechaCita = request.POST["txtFechaCita"]
        horaCita = request.POST["txtHoraCita"]
        sintomasCita = request.POST["txtSintomasCita"]
        try:
            
            if servicio.serDirigido == "Animales Domesticos":
                mascota = Mascota.objects.get(pk=idMascota)
            user = request.user
            
            
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
                if servicio.serDirigido == "Animales Domesticos":
                    cita = Cita.objects.create(
                        ciMascota=mascota,
                        ciServicio=servicio,
                        ciUsuario=user,

                        ciFecha=fechaCita,
                        ciHora=horaCita,
                        ciSintomas=sintomasCita,
                        ciEstado='Solicitada'  
                    )
                    cita.save()
                    mensaje = "Cita agregada correctamente"
                else:
                    cita = Cita.objects.create(
                        ciServicio=servicio,
                        ciUsuario=user,
                        ciFecha=fechaCita,
                        ciHora=horaCita,
                        ciSintomas=sintomasCita,
                        ciEstado='Solicitada' 
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
            categorias = Categoria.objects.all()[:7]
            proveedores = Proveedor.objects.all()[:6]
            servicios = Servicio.objects.all()[:6]
            return render(request, 'procesoCompra.html', {'usuario': usuario, 
                                                          'productos_en_carrito': productos_en_carrito, 
                                                          'total': total,
                                                          'cantidad_total_productos': cantidad_total_productos,
                                                        'categoria': categorias, 
                                                        'proveedores': proveedores, 
                                                        'servicios': servicios})
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
                total_carrito, descuentos_DeTodosLos_productos  = carrito.total_carrito()
                total_pagar = total_carrito
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
                    
                    metodo_pago = metodo_pago or "Sin especificar"
                    
                    envio = DetellaEnvio.objects.create(detNombreDestinatario = nombre_completo,
                                         detNitDestinatario = numero_identificacion,
                                         detDescripcion = descripcion_direccion,
                                         detDepartamento = departamento,
                                         detMunicipio = municipio,
                                         detDireccion = direccion,
                                         detTelefonoDestinatario = telefono,
                                         detCorreoDestinatario = correo_electronico 
                                         )
                    
                    fecha = datetime.now()
                    fecha_actual = datetime.strftime(fecha, "%Y-%m-%d")
                    colombia_timezone = pytz.timezone('America/Bogota')
                    # Obtener la hora actual en Colombia
                    hora_colombiana = datetime.now(colombia_timezone).strftime("%H:%M:%S")
                    carro = Carrito(request)
                    
                    
                    descuentos_Detodos_____Pro = descuentos_DeTodosLos_productos
                    pedido = Pedido.objects.create(
                        peUsuario=usuario,
                        peEstado=estado_pedido,
                        peCodigoPedido= codigoPedido,
                        peImpuestoPedido=impuesto,
                        peTotalPedido=total_pagar,
                        peDescuento = descuentos_DeTodosLos_productos,
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
                        precioPorElcualSeVendio = value["precioUnidad"]
                        if producto.proEstado == "Promocion":
                            
                            descuentoPorcentaje = value["porcentajeDescuento"]
                            descuentoUnidad = value["descuento"]
                            precioTotalPorElDescuento = cantida * descuentoUnidad
                            detallePdf.append([str(producto.proNombre), cantida, str(producto.proPrecio), totalProductoCantidad])
                            DetallePe =DetallePedido.objects.create(detCantida = cantida,  
                                                                    detPrecio = totalProductoCantidad, 
                                                                    detProducto = producto,
                                                                    detPedido = pedido,
                                                                    detDescuentoPorcentaje = descuentoPorcentaje,
                                                                    detDescuentoPrecio = precioTotalPorElDescuento,
                                                                    detPrecioVendidoProducto = precioPorElcualSeVendio
                                                                    )
                            DetallePe.save()
                        else:
                            
                            detallePdf.append([str(producto.proNombre), cantida, str(producto.proPrecio), totalProductoCantidad])
                            DetallePe =DetallePedido.objects.create(detCantida = cantida,  
                                                                    detPrecio = totalProductoCantidad, 
                                                                    detProducto = producto,
                                                                    detPedido = pedido,
                                                                    detDescuentoPorcentaje = 0,
                                                                    detDescuentoPrecio = 0,
                                                                    detPrecioVendidoProducto = precioPorElcualSeVendio
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
                        Recuerda subir una imagen del comprobante de pago en la plataforma, correo, o nuestro whatsapp.<br>\
                        <br>\
                        <b>Detalle del pedido</b><br> \
                        {tabla}'
                    destinatarios = [correo_electronico, usuario.email]
                    
                    thread = threading.Thread(target=enviarCorreoDosDestinatarios, args=(asunto,mensaje, destinatarios, archivo))
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
    # archivo_path = os.path.join('/home/veterinariaAnimalagro/GestionVeterinaria/GestionVeterinaria/media', archivo_nombre)
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
    # archivo_path = os.path.join('/home/veterinariaAnimalagro/GestionVeterinaria/GestionVeterinaria/media', archivo_nombre)
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
                "precioUni": det.detPrecioVendidoProducto,
                "cantidad": det.detCantida,
                "descuento": det.detDescuentoPrecio,
                "porcentaje": det.detDescuentoPorcentaje,
                "precio": det.detPrecio
            }
            lista_detalles.append(detalle)  
        
        pedido = {
            "idPedido": ped.pk,
            "foto": str(ped.proFotoComprobante),
            "estado": ped.peEstado
        }
        envioDet={
            "detNombre": f"{ped.peDetEnvio.detNombreDestinatario}",
            "detTelefono": ped.peDetEnvio.detTelefonoDestinatario,
            "detCorreo": f"{ped.peDetEnvio.detCorreoDestinatario}",
            "detDireccion": f"{ped.peDetEnvio.detDireccion}",
            "detUbicacion": f"Departamento: {ped.peDetEnvio.detDepartamento}, Municipio: {ped.peDetEnvio.detMunicipio}"
        }
        listaEnviodet = [envioDet]
        retorno = {"detalle": lista_detalles, "estado": True, "ped": pedido, "estado": estadoPedido, "envio": listaEnviodet}
        return JsonResponse(retorno)
    except Exception as er:
        print(er)



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
        limite = 6
        if nombreM != "" and fotoM != "" and razaM != "" and tipoM != "":

            usuario_actual = request.user
            mascotas_count = Mascota.objects.filter(masUser = usuario_actual).count()
            # Crear una nueva instancia del modelo Mascota con los datos recibidos y el usuario actual
            if mascotas_count < limite: 
                nueva_mascota = Mascota.objects.create(masNombre=nombreM, masFoto=fotoM, masRaza=razaM, masTipoAnimal=tipoM, masUser=usuario_actual)
                nueva_mascota.save()  # Guardar la mascota en la base de datos
                Mensaje = "Mascota agregada correctamente"
                estado = True
                retorno = {
                    "mensaje": Mensaje, "estado": estado
                }
                return JsonResponse(retorno)
            else: 
                Mensaje = "Ya superaste el limite de mascotas agregadas"
                estado = False
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
            codigo = pedido.peCodigoPedido
            descripcion = pedido.peDetEnvio.detDireccion
            archivo = generaPdfPedido(codigo, descripcion )
            if pedido.peEstado != "Rechazado" or pedido.peEstado != "Cancelado":
                asunto='Verificacion Del Pedido Sistema Veterinaria Animalagro'
                mensaje=f'Cordial saludo, <b>{pedido.peUsuario.first_name} {pedido.peUsuario.last_name}</b>, nos permitimos,\
                    informarle que su pedido esta en proceso de verificacion, por lo cual el estado del pedido cambio a <b>{pedido.peEstado}</b>. \
                    Codigo Del Pedido: {pedido.peCodigoPedido}'
                thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, pedido.peUsuario.email) )
                thread.start()
            
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
        print(telefono)
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
            print(user.userTelefono)
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
            usuarios = User.objects.filter(userEmpleado=None)
            retorno = []
            for em in empleados: 
                usuariosEm = User.objects.filter(userEmpleado=em)
                for usuario in usuariosEm:
                    li = {
                        "id": usuario.id,
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
            con = Contactanos.objects.all().values()
            for contacto in con:
                if contacto['conFecha']:
                    contacto['conFecha'] = contacto['conFecha'].strftime('%Y-%m-%d')
                if contacto['conHora']:
                    contacto['conHora'] = contacto['conHora'].strftime('%H:%M:%S')
            contactos_json = json.dumps(list(con))
            cuerpo = {
                "contactanos": Contactanos.objects.all().count(),
                "contacto":Contactanos.objects.all(),
                "contactos_json":contactos_json,
                "user": request.user, 
                "rol": rol,
                "ventashoy": ventashoy,
                "empleados_info": retorno,
                "users": usuarios
            }

            return render(request, "Administrador/listarUsuarios.html", cuerpo)

    else:
        return render(request, 'Error/403.html')
def responderMensajeCOntactanos(request, id):
    try:
        contac = Contactanos.objects.get(pk = id)
        res = request.POST["Responder"]
        contac.conResponder = res
        contac.save()
        asunto='Recordatorios, Sistema Veterinaria Animalagro'
        mensaje = f'Cordial saludo, <b>{contac.conNombre}</b>.\
        Hemos visto tu motivo de contactarnos, aqui la respuesta</b>.\
        Respuesta: <b>{contac.conResponder}</b>.\
        '

        thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje,contac.conEmail ) )
        thread.start()
        
        return redirect('/listarUsuarios/')
    except Exception as e:
        print(e)
def Suspende_Activar_Usuario(request, id, mensaje):
    try:
        idUsuario = id
        estado = mensaje
        print(estado)
        with transaction.atomic():
            user = User.objects.get(pk = idUsuario)
            user.userEstado = estado
            user.save()
            retorno = {
                "mensaje": "Estado Actualizado Correctamente",
                "estado": True
            }
            return JsonResponse(retorno)
        
    except Exception as er:
        transaction.rollback()
        retorno = {
                "mensaje": "Error al actualizar el estado",
                "estado": False
        }
        return JsonResponse(retorno)
    
def editaSersvicioAdministradro(request, id):
    try:
        nombre = request.POST["nombreEdit"]
        tipo = request.POST["tipoEdit"]
        descripcion = request.POST["descripcionEdit"]
        precio = request.POST["precioEdit"]
        estado = request.POST["estadoEdit"]
        idEmpleado = int(request.POST["empleadoEdit"])
        animalDirigido = request.POST["animalEdit"]
        ideServicio = id
        print(animalDirigido)
        with transaction.atomic():
            servicio = Servicio.objects.get(pk = ideServicio)
            if nombre:
                servicio.serNombre = nombre
            if tipo:
                servicio.serTipo = tipo
            if descripcion: 
                servicio.serDescripcion = descripcion
            if precio:
                servicio.serPrecio = precio
            if estado != 0: 
                servicio.serEstado = estado
            if idEmpleado != 0 and idEmpleado != 9999999999999:
                empleado = Empleado.objects.get(pk = idEmpleado)
                servicio.serEmpleado = empleado
            if idEmpleado == 9999999999999:
                servicio.serEmpleado= None
            if animalDirigido != "e":
                servicio.serDirigido = animalDirigido
            servicio.save()
            
            retorno = {
                "mensaje": "Servicio editado correctamente",
                "estado": True
            }
            
            return JsonResponse(retorno)
    except Exception as er:
        transaction.rollback()
        print(er)
        retorno = {
                "mensaje": "Error al editar, intentelo mas tarde",
                "estado": False
            } 
        return JsonResponse(retorno)
    
def mostrarEditarServicio(request, id):
    try:
        ide = id
        servicio = Servicio.objects.get(pk = ide)
        listaServicio = {
            "id":servicio.id,
            "serNombre": servicio.serNombre,
            "serTipo": servicio.serTipo,
            "serDescripcion": servicio.serDescripcion, 
            "serPrecio": servicio.serPrecio, 
            "serEstado": servicio.serEstado,
            "serDirigido":servicio.serDirigido,
            "serEmpleado": None,
            "serNombreEmpleado": None,
            "serEmpleadoCargo": None
        }
        
        if servicio.serEmpleado != None:
            listaServicio["serEmpleado"] = servicio.serEmpleado.id
            listaServicio["serNombreEmpleado"] = f"{servicio.serEmpleado.emNombre} {servicio.serEmpleado.emApellido}"
            listaServicio["serEmpleadoCargo"] = servicio.serEmpleado.emCargo
        
        listaEm =[]
        for e in Empleado.objects.all():
            em = {
                "id": e.id,
                "nombre": f"{e.emNombre} {e.emApellido}",
                "cargo": e.emCargo
            }
            
            listaEm.append(em)
        retorno = {
            "servicio": listaServicio, "estado": True, "lista": estadDelServicio, "empleado": listaEm,
            "animalDirigido": servicioDirigido_animales
        }
        
        return JsonResponse(retorno)
        
    except Exception as e:
        print(e)

def enviarCorreosDeRecordatorioAtodas(request):
    try:
        citas = None
        citas = Cita.objects.filter(ciEstado = "Solicitada")
        if citas != None:
            for c in citas:
                asunto='Recordatorios, Sistema Veterinaria Animalagro'
                mensaje = f'Cordial saludo, <b>{c.ciUsuario.first_name} {c.ciUsuario.last_name}</b>.\
                Queremos recordarte sobre tu cita programada para el día <b>{c.ciFecha} a las {c.ciHora}</b>.\
                Esperamos verte a ti y a tu querida mascota: <b>{c.ciMascota.masNombre}</b>.'

                thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje,c.ciUsuario.email ) )
                thread.start()
            retorno =  {
                "estado": True, 
                "mensaje": "Recordatorios Enviados Correctamente"
            }
            return JsonResponse(retorno)
        else:
            retorno =  {
                "estado": False, 
                "mensaje": "No hay citas para enviar recordatorios"
            }
            return JsonResponse(retorno)
    except Exception as er:
        retorno={
            "estado": False, 
            "mensaje": "Erro al enviar los recordatorios"
        }
        
        return JsonResponse(retorno)

def recordatorioDeCitaPersonalizado(request, id):
    try:
        citas = None
        idCita = id
        citas = Cita.objects.get(ciEstado = "Solicitada", pk = idCita )
        if citas != None:
            asunto='Recordatorios, Sistema Veterinaria Animalagro'
            mensaje = f'Cordial saludo, <b>{citas.ciUsuario.first_name} {citas.ciUsuario.last_name}</b>.\
            Queremos recordarte sobre tu cita programada para el día <b>{citas.ciFecha} a las {citas.ciHora}</b>.\
            Esperamos verte a ti y a tu querida mascota: <b>{citas.ciMascota.masNombre}</b>.'

            thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje,citas.ciUsuario.email ) )
            thread.start()
            retorno =  {
                "estado": True, 
                "mensaje": "Recordatorio Enviado Correctamente"
            }
            return JsonResponse(retorno)
        else:
            retorno =  {
                "estado": False, 
                "mensaje": "No existe la cita"
            }
            return JsonResponse(retorno)
        
    except Exception as er:
        retorno={
            "estado": False, 
            "mensaje": "Erro al enviar los recordatorios"
        }
        
        return JsonResponse(retorno)
    
def detalleDeLaCitaMascota(request, id):
    try:
        mascota = Mascota.objects.get(pk = id)
        citas = Cita.objects.filter(ciMascota = mascota)
        lista = []
        for c in citas:
            listCitas = {
                "ciServicio": f"{c.ciServicio.serNombre}",
                "ciPrecio": f"{c.ciServicio.serPrecio}", 
                "ciFecha": f"{c.ciFecha} - {c.ciHora}",
                "ciEstado": f"{c.ciEstado}",
                "ciVeterinario": "No hay Empleado",
                "ciPdf": True
            }
            if c.ciServicio.serEmpleado != None:
                listCitas["ciVeterinario"]= f"{c.ciServicio.serEmpleado.emNombre} {c.ciServicio.serEmpleado.emApellido}"
            if c.ciEstado == "Atendida":
                fecha = c.ciFecha.strftime('%Y-%m-%d')
                hora = c.ciHora.strftime('%H-%M-%S')
                nombre = f"historial-{fecha}-{hora}.pdf"
                
                urlPath = os.path.join('/media/', nombre)
                print(urlPath)
                listCitas["ciPdf"]= f"{urlPath}"
                
            lista.append(listCitas)
            
        return JsonResponse({"cita": lista, "estado": True})
    
    except Exception as er:
        print(er)