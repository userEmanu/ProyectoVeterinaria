from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings 
from django.utils import timezone
import pytz


estadoUsuario= [
    """_summary_
    Estados del usuario para saber si esta habilitado para usar el aplicativo iniciando sesión
    """
    ('Activo','Activo'), ('Suspendido', 'Suspendido')
]

tiposUsuarios=[
    """
    Tipo De Usuarios
    """
    ('Usuario', 'Usuario'), ('Empleado','Empleado'), ('Administrador', 'Administrador')
]

estadoCita=[
    """_summary_
    Estados de la citas
    """
    ('Solicitada', 'Solicitada'), ('Atendida', 'Atendida'), ('Cancelada', 'Cancelada')
]

estadoProducto=[
    """_summary_
    Los estados de los productos, en el aplicativo web, solo se muestran los productos que estan en
    'Disponible' y en 'Promocion', y en la aplicacion movil solo los que estan en estado 'Disponible'
    """
    ('Disponible', 'Disponible'), ('Agotado','Agotado'), ('Vencido', 'Vencido'), ('Eliminado','Eliminado'), ('Promocion','Promocion')
]



metodoPago=[
    """_summary_
    Metodos de pagos
    """
    ('PSE', 'PSE'),('Bancolombia', 'Bancolombia'), ('Nequi','Nequi') 
]

estadoPedido=[
    """_summary_
    Estados de los pedidos 
    """
    ('Enviado','Enviado'), ('Entregado', 'Entregado'), ('Solicitado', 'Solicitado'), ('Rechazado', 'Rechazado'), ('Cancelado','Cancelado'), ('Pago Cargado','Pago Cargado')
]

saberEmpleadoUsuario=[
    """_summary_
    Saber si un empleado ya tiene un usuario o no
    """
    ('Creado', 'Creado'), ("SinCrear","SinCrear")
]
tipoDocumento = [
    """_summary_
    Tipo de documentos permitidos para el registro del sistema de los usuarios y emplados
    """
    ('TI', 'Tarjeta Identidad'), ('CC','Cedula Ciudadania'), ('CCE', 'Cedula Extranjera')
]

servicioDirigido_animales = [
    """_summary_
    A que tipo de animal va dirigido el servicio o en que tipo de animales se especializa el servicio
    """
    ('Animales Domesticos', 'Animales Domesticos'), ('Animales De Granja', 'Animales De Granja')
]
estadDelServicio=[
    """_summary_
    Estados de los servicios, solo se muestra los que estan en disponible
    """
    ('Disponible', 'Disponible'),('NoDisponible', 'NoDisponible')
]
class Empleado(models.Model):
    """_summary_

    Args:
        models (_type_): Empleado
        Modelo de los empleados que tiene la veterinaria, solo los agregar el usuario con el rol administrador
    """
    emNombre = models.CharField(max_length=40, null=False, db_comment="Nombres Completos del empleado")
    emApellido = models.CharField(max_length=40, null=False, db_comment="Apellidos Completos del empleado")
    emTelefono = models.BigIntegerField( null=False, db_comment="Numero telefonico del empleado")
    emDireccion = models.CharField(max_length=40, null=False, db_comment="Direccion de residencia")
    emTipoDoc = models.CharField(max_length=5, null=False, db_comment="Tipo de identificacion")
    emNumeroDoc = models.IntegerField( null=False, unique=True, db_comment="Numero de identificacion")
    emCargo = models.CharField(max_length=30, null=False, db_comment="Nombre del cargo que ejerce")
    emCorreo = models.CharField(max_length=48, null=False, unique=True, db_comment="Direccion del correo electronico")
    emUsuario = models.CharField(max_length=13,choices=saberEmpleadoUsuario, null= True, default= "SinCrear")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    

class DetellaEnvio(models.Model):
    """_summary_

    Args:
        models (_type_): Detalle envio
        Es el detalle del envio de un pedido
    """
    detNombreDestinatario = models.CharField(max_length=60, null=False, db_comment="Nombre de aquien se envia")
    detNitDestinatario = models.IntegerField( null=False, db_comment="tipo de documento a quien se envia")
    detDescripcion = models.TextField(max_length=200, null=True, db_comment = "Descripcion de la direccion")
    detDepartamento = models.CharField(max_length=20, null=True, db_comment="Departamento")
    detMunicipio = models.CharField(max_length=20, null=True, db_comment="Municipio")
    detDireccion= models.CharField(max_length=20, null=True, db_comment="Direccion")
    detTelefonoDestinatario = models.BigIntegerField( null=False, db_comment= "Telefono del quien recibe")
    detCorreoDestinatario = models.CharField(max_length=30, null=False, db_comment ="correo del destinatario")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

class Proveedor(models.Model):
    """_summary_

    Args:
        models (_type_): Proveedor
        El modelo del proveedor de un producto
    Returns:
        _type_: _description_
    """
    proNombre = models.CharField(max_length=40, null=False, db_comment="Nombre de la empresa")
    proRepresentante = models.CharField(max_length=40, null=False, db_comment= "Nombre del representante legar de la empresa")
    proDireccion = models.CharField(max_length=40, null=False, db_comment="Direccion de la empresa")
    proTelefono = models.BigIntegerField( null=False, db_comment="Telefono de la empresa")
    proNit = models.IntegerField( null=False, db_comment="NIT de la empresa")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self):
        return f"{self.proNombre}"

class Categoria(models.Model):
    """_summary_

    Args:
        models (_type_): Categoria
        Modelo de categoria del producto

    Returns:
        _type_: _description_
    """
    catNombre = models.CharField(max_length=30, null=False, unique=True, db_comment="Nombre de la categoria")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    def __str__(self):
        return f"{self.catNombre}"
    
    

    
class User(AbstractUser):
    """_summary_

    Args:
        AbstractUser (_type_): User
        Modelo del usuario
    Returns:
        _type_: _description_
    """
    userTipoDoc = models.CharField(max_length=8, choices=tipoDocumento, null=False, db_comment="Tipo de Documento")
    userEstado = models.CharField(max_length=11, choices= estadoUsuario, null=False, db_comment="Estado del usuario", default="Activo")
    userNoDoc = models.IntegerField( null=True, unique=True, db_comment="Numero de documento")
    userTelefono = models.BigIntegerField(null=True, db_comment='Telefono del usuario')
    userFoto = models.ImageField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del Usuario")
    userTipo = models.CharField(max_length=15,choices=tiposUsuarios,db_comment="Nombre Tipo de usuario")
    userEmpleado = models.ForeignKey(Empleado, on_delete=models.PROTECT,null=True,db_comment ="id del empleado, solo si el empleado tiene un usuario")
    userCodigo = models.IntegerField(null=True,unique= True, db_comment="Codigo Recuperacion")
    fechaHoraCreacio  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    def __str__(self):
        return f"{self.username}"

class Mascota(models.Model):
    """_summary_

    Args:
        models (_type_): Mascota
        Modelo de las mascotas que tiene un User
    """
    masNombre = models.CharField(max_length=20, null=False, db_comment="Nombre de la mascota")
    masFoto = models.ImageField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto de la mascota")
    masRaza = models.CharField(max_length=30, null=True, db_comment="Raza de la mascota")
    masTipoAnimal = models.CharField(max_length=30, null=True, db_comment="Tipo del animal. Gato, perro etc")
    masUser = models.ForeignKey(User, on_delete=models.PROTECT, null=False, db_comment="Usuario al que pertenece la mascota")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    
class Servicio(models.Model):
    """_summary_

    Args:
        models (_type_): Servicio
        Modelo del Servicio que se da a los animales
    """
    serNombre = models.CharField(max_length=60, null=False, unique=True, db_comment="Nombre del tratamiento")
    serTipo = models.CharField(max_length=40, null=False, db_comment="Tipo de tratamiento, si es cirugia, revision")
    serFoto = models.ImageField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del Servicio")
    serDirigido = models.CharField(max_length=30, choices=servicioDirigido_animales, null=True, db_comment= "A que tipo de animales va dirigido el animal" )
    serEmpleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, null= True,db_comment="El empleado que atiende este servicio")
    serPrecio = models.IntegerField(null=False, db_comment="Precio del Tratamiento")
    serEstado = models.CharField(max_length=13, null=True, choices= estadDelServicio, default= "Disponible")
    serDescripcion = models.TextField(null=False, db_comment = "Descripcion Del servicio")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    
    
class Cita(models.Model):
    """_summary_

    Args:
        models (_type_): Cita
        Modelo de Cita, modelo de todas la citas que puede agendar un usuario, con su respectiva mascota 
        dependiendo si el servicio va dirigido animales domesticos o animales de granja
    """
    ciDescripcion = models.TextField(max_length=500, null=True, db_comment ="Descripcion de la cita despues de ser atendida")
    ciSintomas = models.CharField(max_length=50, null=False, db_comment="sintomas de la mascota")
    ciEstado = models.CharField(max_length=20, choices=estadoCita, db_comment="Estado de la cita", null=False)
    ciFecha = models.DateField(null=True, db_comment="Fecha de la cita")
    ciHora = models.TimeField(null=True, db_comment="Hora de la cita")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    ciMascota = models.ForeignKey(Mascota, on_delete=models.PROTECT, db_comment="Macota", null=True)
    ciServicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, null=True, db_comment="Servicio")
    ciUsuario = models.ForeignKey(User, on_delete=models.PROTECT, null=False, db_comment="Usuario")
    
class Producto(models.Model):
    """_summary_

    Args:
        models (_type_): Producto
        Modelo del producto
    """
    proNombre = models.CharField(max_length=50, null=False, db_comment=" Nombre del prooducto")
    proEstado = models.CharField(max_length=20, choices=estadoProducto, db_comment="Estado del produco")
    proPrecio = models.IntegerField( null=False, db_comment = "Precio del producto")
    proFoto = models.FileField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del Producto")
    proDescripcion = models.TextField(max_length=600, null=False, db_comment="Descripcion del producto")
    proDescuento = models.IntegerField(null=True, default=0,db_comment= "Porcentaje del descuento, del 1 a 100")
    proProveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, db_comment="Proveedor")
    proCategoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, db_comment="Categoria")
    proCantidad = models.BigIntegerField(null=True, default=0, db_comment="Cantidad_Disponible")
    proCantidadVendida = models.BigIntegerField(null=True, default=0, db_comment="Cantidad_Disponible")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraCaducidad = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

class Pedido(models.Model):
    """_summary_

    Args:
        models (_type_): Pedido
        Modelos de los pedido de un usuario con rol tipo usuario, toda informacion posible
    """
    peUsuario = models.ForeignKey(User, on_delete=models.PROTECT, db_comment="Usuario que hizo el pedido")
    peEstado = models.CharField(max_length=14, null=False, choices=estadoPedido, db_comment="estado del pedido")
    peCodigoPedido = models.IntegerField(null=True, db_comment ="Codigo del comprobante", unique=True) 
    peImpuestoPedido = models.IntegerField( null=True, db_comment="Impuesto del pedido")
    peTotalPedido = models.IntegerField(null=True, db_comment="Total pedido")
    peFecha = models.DateField(null=True,db_comment="Fecha pedido")
    peDescuento = models.IntegerField(null=True, db_comment="DescuentoTotal")
    peHora = models.TimeField(null=True,db_comment="Hora pedido")
    proFotoComprobante = models.ImageField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del comprobante")    
    peFormaPago = models.CharField(max_length=20,null=False, db_comment="Forma de pago")
    peDetEnvio = models.ForeignKey(DetellaEnvio, on_delete=models.PROTECT, db_comment="Detalle ENVIO")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
class DetallePedido(models.Model):
    """_summary_

    Args:
        models (_type_): Detalle del pedido
        Detalle del pedido, aqui va los productos que pidio en el pedido
    """
    detCantida = models.IntegerField( null=False, db_comment="Cantidad del producto")
    detDescuentoPrecio = models.IntegerField(null=True, db_comment="Precio Del Descuento")
    detDescuentoPorcentaje = models.IntegerField(null=True, db_comment= "Descuento Porcentaje")
    detPrecioVendidoProducto = models.IntegerField(null=True, db_comment="Precio Por el que se vendio el producto")
    detPrecio = models.IntegerField(null=False, db_comment ="Precio por cada producto con descuento")
    detProducto = models.ForeignKey(Producto, on_delete=models.PROTECT, db_comment="Producto")
    detPedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, db_comment="Detalle envio", null=True)
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    

    
class Contactanos(models.Model):
    """_summary_

    Args:
        models (_type_): Contactanos
        Modelo de contactanos, si no esta registrado se puede contactar
    """
    conNombre = models.CharField(max_length=50, null=False, db_comment=" Nombre De La Persona Que Se Va Contactar")
    conEmail = models.CharField(max_length= 30, null=False,  db_comment="Direccion del correo electronico")
    conNumeroTe = models.BigIntegerField( null=True, db_comment="Telefono del usuario Que Se Contacta")
    conMensaje = models.CharField(max_length=150, null=True, db_comment="Mensaje Que El Usuario enviar para contartacnos")
    conFecha = models.DateField(null= True, db_comment="Fecha en la que registro el mensaje")
    conHora = models.TimeField(null=True, db_comment="Hora en la que registro el mensjae")
    conResponder = models.TextField(max_length=200, null=True, db_comment="Respuesta por parte del administrador")
   

# Group.objects.get_or_create(name='Usuario')
# Group.objects.get_or_create(name='Administrador')
# Group.objects.get_or_create(name='Asistente')
# Group.objects.get_or_create(name='Medico')