from rest_framework import generics
from appVeterinaria.models import *
from appVeterinaria.serializers import *
from django.http import JsonResponse
from django.core import serializers
from django.contrib import auth
from django.http import HttpResponse
import json
import pytz
import random
from django.db.models import Count
from django.db.models import Q
from datetime import date, datetime, time, timedelta
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import base64
from django.core.files.base import ContentFile
from appVeterinaria.views import generaPdfPedido, enviarCorreo
# Listas
class userList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class empleadoList(generics.ListCreateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class detalleEnvioList(generics.ListCreateAPIView):
    queryset = DetellaEnvio.objects.all()
    serializer_class = DetalleEnvioSerializer

class proveedorList(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class categoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
class mascotaList(generics.ListCreateAPIView):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

class citaList(generics.ListCreateAPIView):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer

class productoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class detallePedidoList(generics.ListCreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetalleEnvioSerializer


    
    
# lista Por Id


class userDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class empleadoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class detalleEnvioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetellaEnvio.objects.all()
    serializer_class = DetalleEnvioSerializer

class proveedorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class categoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
class mascotaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mascota.objects.filter()
    serializer_class = MascotaSerializer

class citaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer

class productoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class detallePedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetalleEnvioSerializer



def loginGET(request,userName,password):
    if request.method == 'GET':
        queryset = authenticate(request,username=userName, password = password)
        if queryset is not None:
            auth.login(request, queryset)
            serialized_data = serializers.serialize('json', [queryset]) 
            return JsonResponse(serialized_data, safe=False)
        else:
            return HttpResponse("ERROR USUARIO NO ENCONTRADo,  GET")  
    else:
        return HttpResponse("error INTERNO")     


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self ,request):
            username = request.data.get("username", None)
            password = request.data.get("password", None)
            user = authenticate(username=username, password=password)
            if user and user.userEstado == "Activo" :
                if user.groups.filter(name__in=('Usuario', 'Administrador')):
                    login(request, user)
                    return Response(UserSerializer(user).data, status = status.HTTP_200_OK)
                else:
                    return Response(status = status.HTTP_404_NOT_FOUND)
            else:
                return Response(status = status.HTTP_404_NOT_FOUND)
            
        


@method_decorator(csrf_exempt, name='dispatch')
class aggMascotaView(APIView):
    def post(self, request):
        ide = request.data.get("id", None)
        tipo = request.data.get("tipo", None)
        raza = request.data.get("raza", None)
        nombre = request.data.get("nombre", None)
        foto = request.data.get("foto", None)

        try:
            usuario = User.objects.get(pk=ide)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        cantidad = Mascota.objects.filter(masUser = usuario).count()
        if cantidad < 6:
            mascota = Mascota.objects.create(masNombre=nombre, masRaza=raza,
                                            masTipoAnimal=tipo, masUser=usuario)

            if foto:
                image_data = base64.b64decode(foto)
                mascota.masFoto.save('fotoMascota.png', ContentFile(image_data), save=True)

            return Response(MascotaSerializer(mascota).data, status=status.HTTP_201_CREATED)
        else: 
            return Response(status=status.HTTP_404_NOT_FOUND)
class informacionAdministradorGraficas(APIView):
    def get(self, request):
        
        fecha_actual = timezone.now()


        fecha_inicio_semana = fecha_actual - timedelta(days=7)

        # Consulta para obtener las ventas de la semana
        ventas_semana = DetallePedido.objects.filter(
            detPedido__peFecha__range=[fecha_inicio_semana, fecha_actual], detPedido__peEstado = "Entregado"
        ).aggregate(total_ventas=Sum('detPrecio'))['total_ventas']
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        ventasDeHoy = Pedido.objects.filter(peFecha=fecha_actual).count()
        compras_usuarios_mes = usuariosQueCompraronEnMesActual() 
        jsonRetornoGraficas = {
            "PedidosHoy": ventasDeHoy, 
            "ComprasUsuarioMes": compras_usuarios_mes, 
            "GananciasSemana": ventas_semana
        }
        return JsonResponse(jsonRetornoGraficas, safe=False)
    
class informacionAdministradorPedidos(APIView):
    def get(self, request):
        pedidosFaltantes = Pedido.objects.filter(peEstado__in=('Pago Cargado', 'Enviado'))
        jsonRetornoPedidos = []
        for p in pedidosFaltantes: 
            lista = {
                "peFecha": f"{p.peFecha} {p.peHora}",
                "peCodigo": p.peCodigoPedido,
                "urlPedido": f"https://veterinariaanimalagro.pythonanywhere.com/media/pedido-{p.peCodigoPedido}.pdf"
            }
            jsonRetornoPedidos.append(lista)

        return JsonResponse(jsonRetornoPedidos, safe=False)
        
class informacionAdministradorCitas(APIView):
    def get(self, request):
        citasFaltantes =Cita.objects.filter(ciEstado='Solicitada')
        jsonRetornoCitas = []
        for c in citasFaltantes:
            citasLista ={
                "ciServicio": c.ciServicio.serNombre, 
                "ciFecha": f"{c.ciFecha} {c.ciHora}",
                "ciUsuario": f"{c.ciUsuario.first_name} {c.ciUsuario.last_name}",
                "ciEmpleado": f"No hay Empleado Asignado"
            }
            if c.ciServicio.serEmpleado != None:
                citasLista["ciEmpleado"] = f'{c.ciServicio.serEmpleado.emNombre} {c.ciServicio.serEmpleado.emApellido}'
                
            jsonRetornoCitas.append(citasLista)
        
        return JsonResponse(jsonRetornoCitas, safe=False)
    
class informacionAdministrador(APIView):
    def get(self, request):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        # Graficas
        ventasDeHoy = Pedido.objects.filter(peFecha=fecha_actual).count()
        ganancias_mes_por_mes = gananciasMensuales()  
        compras_usuarios_mes = usuariosQueCompraronEnMesActual() 
        
        # Ventas Detalladas
        pedidosFaltantes = Pedido.objects.filter(peEstado__in=('Pago Cargado', 'Enviado'))
        

        citasFaltantes = citasQueFaltanPorAtender()
        
        jsonRetornoGraficas = {
            "PedidosHoy": ventasDeHoy, 
            "GananciasMes": ganancias_mes_por_mes,  
            "ComprasUsuarioMes": compras_usuarios_mes  
        }

        jsonRetornoPedidos = []
        for p in pedidosFaltantes: 
            lista = {
                "peFecha": f"{p.peFecha} {p.peHora}",
                "peCodigo": p.peCodigoPedido,
                "urlPedido": f"https://veterinariaanimalagro.pythonanywhere.com/media/pedido-{p.peCodigoPedido}.pdf"
            }
            jsonRetornoPedidos.append(lista)

        jsonRetornoCitas = []
        for c in citasFaltantes:
            citasLista ={
                "ciServicio": c.ciServicio.serNombre, 
                "ciFecha": f"{c.ciFecha} {c.ciHora}",
                "ciUsuario": f"{c.ciUsuario.first_name} {c.ciUsuario.last_name}",
                "ciEmpleado": f"{c.ciServicio.serEmpleado.emNombre} {c.ciServicio.serEmpleado.emApellido}"
            }
            if c.ciServicio.serEmpleado == None:
                citasLista["ciEmpleado"] = None
                
            jsonRetornoCitas.append(citasLista)

        # Retorno JsonApi
        retornoApiJson = {
            "Graficas": jsonRetornoGraficas, 
            "Pedido": jsonRetornoPedidos,
            "Cita": jsonRetornoCitas
        }
        
        return JsonResponse(retornoApiJson, safe=False)

def citasQueFaltanPorAtender(): 
    citas_pendientes = Cita.objects.filter(ciEstado='Solicitada')
    
    return citas_pendientes

def usuariosQueCompraronEnMesActual():
    mes_actual = datetime.now().month

    usuarios_que_compraron = User.objects.filter(pedido__peFecha__month=mes_actual) \
        .annotate(total_pedidos=Count('pedido'))

    cantidadDeUsuarios = usuarios_que_compraron.count()

    return cantidadDeUsuarios

class informacionAdministradorGanancias(APIView):
    def get(self, request):
        meses_espanol = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }

        ganancias_por_mes = Pedido.objects.filter(peEstado='Entregado') \
            .annotate(mes=ExtractMonth('peFecha')) \
            .values('mes') \
            .annotate(ganancias=Sum('peTotalPedido')) \
            .order_by('mes')
        
        ganancias_mensuales = []
        for entrada in ganancias_por_mes:
            mes = entrada['mes']
            ganancias = entrada['ganancias']
            mes_en_espanol = meses_espanol.get(mes, "Desconocido")
            
            lista = {
                "mes": mes_en_espanol,
                "ganancias": ganancias
            }
            ganancias_mensuales.append(lista)

        return JsonResponse(ganancias_mensuales, safe=False)
    

def gananciasMensuales():
    meses_espanol = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }

    ganancias_por_mes = Pedido.objects.filter(peEstado='Entregado') \
        .annotate(mes=ExtractMonth('peFecha')) \
        .values('mes') \
        .annotate(ganancias=Sum('peTotalPedido')) \
        .order_by('mes')
    
    ganancias_mensuales = []
    for entrada in ganancias_por_mes:
        mes = entrada['mes']
        ganancias = entrada['ganancias']
        mes_en_espanol = meses_espanol.get(mes, "Desconocido")
        
        lista = {
            "mes": mes_en_espanol,
            "ganancias": ganancias
        }
        ganancias_mensuales.append(lista)

    return ganancias_mensuales
    
class serviciosListarapi(APIView):
    def get(self, request):
        try: 
            serivicio = Servicio.objects.filter(serEstado = "Disponible")
            listaServicios = []
            for s in serivicio:
                if s.serDirigido == 'Animales Domesticos':
                    serviciosObjeto = {
                        "id": s.id,
                        "serNombre": s.serNombre,
                        "serTipo": s.serTipo, 
                        "serPrecio": s.serPrecio,
                        "serDescripcion": s.serDescripcion,
                        "serEmpleado":{
                            "idEmpleado": s.serEmpleado.id,
                            "serNombre": f"{s.serEmpleado.emNombre} {s.serEmpleado.emApellido}",
                            "serTipo": s.serEmpleado.emCargo
                        }
                    }
                    listaServicios.append(serviciosObjeto)
            return JsonResponse(listaServicios, safe=False)
        except Servicio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class CitasUsuarioApi(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        citas = Cita.objects.filter(ciUsuario=user)
        listaCitas = []

        for ci in citas:
            cita = {
                    "id": ci.id,
                    "CitaEstado": ci.ciEstado,
                    "CitafechaHora": f"{ci.ciFecha} {ci.ciHora}",
                    "urlPdfHistoria":f"https://veterinariaanimalagro.pythonanywhere.com/media/historial-{ci.ciFecha.strftime('%Y-%m-%d')}-{ci.ciHora.strftime('%H-%M-%S')}.pdf",
                    "mascotaNombre": ci.ciMascota.masNombre,
                    "servicioNombre": ci.ciServicio.serNombre
            }
            listaCitas.append(cita)

        if listaCitas:

            return JsonResponse(listaCitas, safe=False)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
class mascotaBuscar(APIView):
    def get(self, request, id):
        user = User.objects.get(pk=id)
        mascota = Mascota.objects.filter(masUser=user)  
        if mascota.exists():
            return Response(MascotaSerializer(mascota, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class productosTodos(APIView):
    def get(self, request):
        productos = Producto.objects.filter(proEstado = "Disponible")
        if productos.exists():
            return Response(ProductoSerializer(productos, many=True).data, status=status.HTTP_200_OK)
        else:
             return Response(status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status = status.HTTP_200_OK)

class ProductoImagen(APIView):
    def post(self,request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            archivo = validated_data['proFoto']
            archivo.name = 'producto.png'
            validated_data['proFoto'] = archivo
            producto = Producto(**validated_data)
            producto.save()
            serializer_response = ProductoSerializer(producto)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MascotaFoto(APIView):
    def post(self,request):
        serializer = MascotaSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            archivo = validated_data['masFoto']
            archivo.name = 'mascota.png'
            validated_data['masFoto'] = archivo
            mascota = Mascota(**validated_data)
            mascota.save()
            serializer_response = MascotaSerializer(mascota)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class AgregarCitaAPI(APIView):
    def post(self, request):
        try:
            try:
                idServicio = request.data.get("idServicio", None)
                idUsuario = request.data.get("idUser", None)
                idMascota = request.data.get("idMascota", None)
                fecha = request.data.get("fecha", None)
                hora = request.data.get("hora", None)
                sintomas = request.data.get("sintomas", None)
                if not (idServicio and idUsuario and idMascota and fecha and hora):
                    return JsonResponse({"error": "Datos de entrada incompletos."}, status=400)
                print(sintomas)
                servicio = Servicio.objects.get(pk=idServicio)
                user = User.objects.get(pk=idUsuario)
                mascota = Mascota.objects.get(pk=idMascota)

                fecha_datetime = datetime.strptime(fecha, "%Y-%m-%d")
                if fecha_datetime.weekday() in [5, 6]: 
                    return JsonResponse({"error": "No se pueden hacer reservas los sábados y domingos."}, status=400)
                
                fecha_cita= datetime.strptime(fecha, "%Y-%m-%d").date()
                hora_cita = datetime.strptime(hora, "%I:%M %p").time()
                
                citas_exist = Cita.objects.filter(
                    ciFecha=fecha_cita, ciHora=hora_cita, ciServicio=servicio
                ).exists()
                
                
                if citas_exist:
                    return JsonResponse({"error": "Ya hay una cita reservada con el mismo veterinario y hora."}, status=400)
                else:
                    cita = Cita.objects.create(
                        ciMascota=mascota,
                        ciServicio=servicio,
                        ciUsuario=user,
                        ciFecha=fecha_cita,
                        ciHora=hora_cita,
                        ciSintomas=sintomas,
                        ciEstado='Solicitada'
                    )
                    return JsonResponse({"mensaje": "Cita Agregada Correctamente"})
            
            except (Servicio.DoesNotExist, User.DoesNotExist, Mascota.DoesNotExist):
                return JsonResponse({"error": "No se encontró el servicio, usuario o mascota especificados."}, status=400)
        except Exception as er:
            return JsonResponse({"error": "Error interno del servidor."}, status=500)
        
class userFoto(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            archivo = validated_data['userFoto']
            archivo.name = 'fotoUsuario.png'
            validated_data['userFoto'] = archivo
            user = User(**validated_data)
            user.save()
            serializer_response = user(user)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class editarUsuarioView(APIView):
    def post(self, request):
        ide = request.data.get("id", None)
        nombre = request.data.get("first_name", None)
        apellido = request.data.get("last_name", None)
        email = request.data.get("email", None)
        doc = request.data.get("userNoDoc", None)
        telefono = request.data.get("userTelefono", None)
        foto = request.data.get("userFoto", None)

        try:
            user = User.objects.get(pk=ide)

            user.first_name = nombre
            user.last_name = apellido
            user.email = email
            user.userNoDoc = doc
            user.userTelefono = telefono

            if foto:
                image_data = base64.b64decode(foto)
                user.userFoto.save('fotoUsuario.png', ContentFile(image_data), save=True)

            user.save()

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class PedidosUsuarioAPI(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        pedidos = Pedido.objects.filter(peUsuario=user)
        listaPedidos = []
        
        if pedidos.exists():  
            for pedido in pedidos:
                pedido_data = {
                    "id": pedido.id,
                    "peEstado": pedido.peEstado, 
                    "peTotalPedido": pedido.peTotalPedido,
                    "peCodigoPedido": pedido.peCodigoPedido,
                    "peFecha": f"{pedido.peFecha} {pedido.peHora}",
                    "urlPdfPedido": f"https://veterinariaanimalagro.pythonanywhere.com/media/pedido-{pedido.peCodigoPedido}.pdf", 
                }
                listaPedidos.append(pedido_data)

            return JsonResponse(listaPedidos, safe=False)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class AgregarPedidoApiRest(APIView):
    def post(self, request): 
        try:
            estado_pedido = 'Solicitado'
            codigoPedido = generar_codigo_unico_numerico()
            idUsuario = request.data.get("idUser", None)
            metodoDepago = request.data.get("pago", None)
            DireccionDes = request.data.get("direccion", None)
            departamento = request.data.get("departamento", None)
            municipio = request.data.get("municipio", None)
            listaProductos = request.data.get("productos", [])
            
            fecha = datetime.now()
            fecha_actual = datetime.strftime(fecha, "%Y-%m-%d")
            colombia_timezone = pytz.timezone('America/Bogota')
            hora_colombiana = datetime.now(colombia_timezone).strftime("%H:%M:%S")
            # Obtener la hora actual en Colombia
            user = User.objects.get(pk = idUsuario)
            descripcionDelEnvio = f"Departamento: {departamento}, municipio: {municipio}, Direccion: {DireccionDes}"
            detEnvio = DetellaEnvio.objects.create(
                detNombreDestinatario = f"{user.first_name} {user.last_name}",
                detNitDestinatario = user.userNoDoc,
                detDescripcion = descripcionDelEnvio,
                detDepartamento = departamento,
                detMunicipio = municipio,
                detDireccion = DireccionDes,
                detTelefonoDestinatario = user.userTelefono,
                detCorreoDestinatario = user.email 
            )
            pedido = Pedido.objects.create(
                            peUsuario=user,
                            peEstado=estado_pedido,
                            peCodigoPedido= codigoPedido,
                            peFormaPago=metodoDepago,
                            peFecha = fecha_actual,
                            peHora = hora_colombiana,
                            peDetEnvio = detEnvio,
                            peDescuento = 0
                        )
            totalDelPedido = 0
            for producto in listaProductos:
                idProducto = int(producto['id'])
                cantidadDelProducto = producto['cantidad']
                productoCreado = Producto.objects.get(pk = idProducto)
                
                productoCreado.proCantidad -= cantidadDelProducto
                productoCreado.proCantidadVendida += cantidadDelProducto
                if productoCreado.proCantidad <= 0: 
                    productoCreado.proEstado = "Agotado"
                producto.save()
                    
                precioDelProducto = productoCreado.proPrecio
                total = cantidadDelProducto * precioDelProducto
                DetallePe =DetallePedido.objects.create(detCantida = cantidadDelProducto,  
                                                            detPrecio = total, 
                                                            detProducto = productoCreado,
                                                            detPedido = pedido,
                                                            detPrecioVendidoProducto = productoCreado.proPrecio, 
                                                            detDescuentoPrecio = 0,
                                                            detDescuentoPorcentaje = 0
                                                            )
                DetallePe.save()
                totalDelPedido = totalDelPedido + total

            impuesto_porcentaje = 19
            impuesto = int(totalDelPedido * impuesto_porcentaje / 100)
            
            pedido.peImpuestoPedido= impuesto
            pedido.peTotalPedido=totalDelPedido
            pedido.save()
            
            archvi = generaPdfPedido(codigoPedido, DireccionDes)
            import threading
            asunto='Sistema Veterinaria Animalagro'
            mensaje=f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos,\
                informarle que usted ha hecho un pedido, con el codigo: {codigoPedido}, que se ah registrado de forma\
                exitosa, recuerda hacer el proceso de pago, en el pdf estan lo metodos de pago de acuerdo a la forma que hayas elegido, puedes pagar.\
                Recuerda subir una imagen del comprobante de pago en la plataforma, correo, o nuestro numero de whatsapp.<br>'
            thread = threading.Thread(target=enviarCorreo, args=(asunto,mensaje, user.email, archvi))
            thread.start()
            
            retorno = {
                "mensaje": "Pedido exitoso"
            }
            return Response(retorno, status=status.HTTP_200_OK)
        except Exception as er:
            return Response({"Error": "Error De Servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def generar_codigo_unico_numerico(longitud=8):
    numeros = "0123456789"
    codigo = ''.join(random.choice(numeros) for _ in range(longitud))

    while Pedido.objects.filter(peCodigoPedido=codigo).exists():
        codigo = ''.join(random.choice(numeros) for _ in range(longitud))

    return codigo

