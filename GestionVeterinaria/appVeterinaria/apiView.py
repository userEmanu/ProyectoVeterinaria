from rest_framework import generics
from appVeterinaria.models import *
from appVeterinaria.serializers import *
from django.http import JsonResponse
from django.core import serializers
from django.contrib import auth
from django.http import HttpResponse
import json
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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

class pedidoList(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
    
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
    queryset = Mascota.objects.all()
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

class pedidoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

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

            if user:
                login(request, user)
                #UserSerializer(users).data
                return Response(UserSerializer(user).data, status = status.HTTP_200_OK)

            return Response(status = status.HTTP_404_NOT_FOUND)
        
@method_decorator(csrf_exempt, name='dispatch')       
class aggMascotaView(APIView):
    def post(self ,request):
        id = request.data.get("id", None)
        tipo = request.data.get("tipo", None)
        raza  = request.data.get("raza", None)
        nombre = request.data.get("nombre", None)
        
        usuario = User.objects.get(pk = id)
        if usuario != "":
            mascota = Mascota.objects.create(masNombre = nombre, masRaza= raza,
                                             masTipoAnimal = tipo,  masUser = usuario)
            return Response(MascotaSerializer(mascota).data, status= status.HTTP_201_CREATED)
            
        return Response(status = status.HTTP_404_NOT_FOUND)



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