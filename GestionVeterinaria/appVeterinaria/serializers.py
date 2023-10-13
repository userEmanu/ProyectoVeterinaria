from rest_framework import serializers
from appVeterinaria.models import *
from drf_extra_fields.fields import Base64ImageField


"""_summary_
Serializadores de los modelos, lo que hace convertir los modelos en json o diccionario Json
"""

class UserSerializer(serializers.ModelSerializer):
    userFoto = Base64ImageField(required = False)
    class Meta: 
        model = User
        fields = ('__all__')
        
class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Empleado
        fields = ('__all__')

class DetalleEnvioSerializer(serializers.ModelSerializer):
    class Meta: 
        model = DetellaEnvio
        fields = ('__all__')
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Proveedor
        fields = ('__all__')

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Categoria
        fields = ('__all__')

class MascotaSerializer(serializers.ModelSerializer):
    masFoto = Base64ImageField(required = False)
    class Meta: 
        model = Mascota
        fields = ('__all__')
        
class CitaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Cita
        fields = ('__all__')

class ProductoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Producto
        fields = ('__all__')

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = DetallePedido
        fields = ('__all__')

class PedidoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Pedido
        fields = ('__all__')