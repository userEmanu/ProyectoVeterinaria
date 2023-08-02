from rest_framework import generics
from appVeterinaria.models import *
from appVeterinaria.serializers import *
from django.http import JsonResponse
from django.core import serializers
from django.contrib import auth
from django.contrib.auth import authenticate
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

def login(request,userName,password):
    if request.method == 'GET':
        queryset = authenticate(request,username=userName, password = password)
        if queryset is not None:
            auth.login(request, queryset)
            serializerd_data = serializers.serialize('json',queryset)
            return JsonResponse(serializerd_data, safe=False)
    