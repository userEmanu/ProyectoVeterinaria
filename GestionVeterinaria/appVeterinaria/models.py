from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings 
from django.utils import timezone





estadoUsuario= [
    ('Activo','Activo'), ('Suspendido', 'Suspendido')
]

tiposUsuarios=[
    ('Usuario', 'Usuario'), ('Empleado','Empleado'), ('Administrador', 'Administrador')
]

estadoCita=[
    ('Solicitada', 'Solicitada'), ('Atendida', 'Atendida'), ('Cancelada', 'Cancelada')
]

estadoProducto=[
    ('Bueno', 'Bueno'), ('Regular','Regular'), ('Vencido', 'Vencido'), ('Eliminado','Eliminado')
]

tipoCategorias=[
    ('Alimento', 'Alimento'), ('Medicina','Medicina'), ('Accesorio', 'Accesorio')
]

metodoPago=[
    ('PSE', 'PSE'),('Bancolombia', 'Bancolombia'), ('Nequi','Nequi') 
]

estadoPedido=[
    ('Enviado','Enviado'), ('Entregado', 'Entregado'), ('Solicitado', 'Solicitado'), ('Rechazado', 'Rechazado'), ('Cancelado','Cancelado')
]

tipoDocumento = [
    ('TI', 'Tarjeta Identidad'), ('CC','Cedula Ciudadania'), ('CCE', 'Cedula Extranjera')
]
class Empleado(models.Model):
    emNombre = models.CharField(max_length=40, null=False, db_comment="Nombres Completos del empleado")
    emApellido = models.CharField(max_length=40, null=False, db_comment="Apellidos Completos del empleado")
    emTelefono = models.IntegerField( null=False, db_comment="Numero telefonico del empleado")
    emDireccion = models.CharField(max_length=40, null=False, db_comment="Direccion de residencia")
    emTipoDoc = models.CharField(max_length=5, null=False, db_comment="Tipo de identificacion")
    emNumeroDoc = models.IntegerField( null=False, unique=True, db_comment="Numero de identificacion")
    emCargo = models.CharField(max_length=30, null=False, db_comment="Nombre del cargo que ejerce")
    emCorreo = models.CharField(max_length=48, null=False, unique=True, db_comment="Direccion del correo electronico")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    

class DetellaEnvio(models.Model):
    detNombreDestinatario = models.CharField(max_length=40, null=False, db_comment="Nombre de aquien se envia")
    detNitDestinatario = models.IntegerField( null=False, db_comment="tipo de documento a quien se envia")
    detDescripcion = models.TextField(max_length=200, null=False, db_comment = "Descripcion del envio")
    detTelefonoDestinatario = models.IntegerField( null=False, db_comment= "Telefono del quien recibe")
    detCorreoDestinatario = models.CharField(max_length=30, null=False, db_comment ="correo del destinatario")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

class Proveedor(models.Model):
    proNombre = models.CharField(max_length=40, null=False, db_comment="Nombre de la empresa")
    proRepresentante = models.CharField(max_length=40, null=False, db_comment= "Nombre del representante legar de la empresa")
    proDireccion = models.CharField(max_length=40, null=False, db_comment="Direccion de la empresa")
    proTelefono = models.IntegerField( null=False, db_comment="Telefono de la empresa")
    proNit = models.IntegerField( null=False, db_comment="NIT de la empresa")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self):
        return f"{self.proNombre}"

class Categoria(models.Model):
    catNombre = models.CharField(max_length=30, null=False, unique=True, db_comment="Nombre de la categoria")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    def __str__(self):
        return f"{self.catNombre}"
    
    

    
class User(AbstractUser):
    userTipoDoc = models.CharField(max_length=8, choices=tipoDocumento, null=False, db_comment="Tipo de Documento")
    userNoDoc = models.IntegerField( null=True, unique=True, db_comment="Numero de documento")
    userTelefono = models.IntegerField( null=True, db_comment="Telefono del usuario")
    userFoto = models.FileField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del Usuario")
    userTipo = models.CharField(max_length=15,choices=tiposUsuarios,db_comment="Nombre Tipo de usuario")
    userEmpleado = models.ForeignKey(Empleado, on_delete=models.PROTECT,null=True,db_comment ="id del empleado, solo si el empleado tiene un usuario")
    userCodigo = models.IntegerField(null=True,unique= True, db_comment="Codigo Recuperacion")
    fechaHoraCreacio  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    def __str__(self):
        return f"{self.username}"

class Mascota(models.Model):
    masNombre = models.CharField(max_length=20, null=False, db_comment="Nombre de la mascota")
    masFoto = models.FileField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto de la mascota")
    masRaza = models.CharField(max_length=30, null=True, db_comment="Raza de la mascota")
    masTipoAnimal = models.CharField(max_length=30, null=True, db_comment="Tipo del animal. Gato, perro etc")
    masUser = models.ForeignKey(User, on_delete=models.PROTECT, null=False, db_comment="Usuario al que pertenece la mascota")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    
class Servicio(models.Model):
    serNombre = models.CharField(max_length=30, null=False, unique=True, db_comment="Nombre del tratamiento")
    serTipo = models.CharField(max_length=40, null=False, db_comment="Tipo de tratamiento, si es cirugia, revision")
    serEmpleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, null= True,db_comment="El empleado que atiende este servicio")
    serPrecio = models.IntegerField(null=False, db_comment="Precio del Tratamiento")
    serDescripcion = models.TextField(null=False, db_comment = "Descripcion Del servicio")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
    
    
class Cita(models.Model):
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
    proNombre = models.CharField(max_length=50, null=False, db_comment=" Nombre del prooducto")
    proEstado = models.CharField(max_length=20, choices=estadoProducto, db_comment="Estado del produco")
    proPrecio = models.IntegerField( null=False, db_comment = "Precio del producto")
    proFoto = models.FileField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del Producto")
    proDescripcion = models.TextField(max_length=600, null=False, db_comment="Descripcion del producto")
    proProveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, db_comment="Proveedor")
    proCategoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, db_comment="Categoria")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraCaducidad = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")

class Pedido(models.Model):
    peUsuario = models.ForeignKey(User, on_delete=models.PROTECT, db_comment="Usuario que hizo el pedido")
    peEstado = models.CharField(max_length=10, null=False, choices=estadoPedido, db_comment="estado del pedido")
    peCodigoPedido = models.IntegerField(null=True, db_comment ="Codigo del comprobante", unique=True) 
    peImpuestoPedido = models.IntegerField( null=True, db_comment="Impuesto del pedido")
    peTotalPedido = models.IntegerField(null=True, db_comment="Total pedido")
    proFotoComprobante = models.FileField(upload_to=f"fotos/", null=True, blank=True,db_comment="Foto del comprobante")    
    peFormaPago = models.CharField(max_length=20,null=False, db_comment="Forma de pago")
    peDetEnvio = models.ForeignKey(DetellaEnvio, on_delete=models.PROTECT, db_comment="Detalle ENVIO")
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,db_comment="Fecha y hora última actualización")
    
class DetallePedido(models.Model):
    detCantida = models.IntegerField( null=False, db_comment="Cantidad del producto")
    detPrecio = models.IntegerField(null=False, db_comment ="Precio por cada producto")
    detProducto = models.ForeignKey(Producto, on_delete=models.PROTECT, db_comment="Producto")
    detPedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, db_comment="Detalle envio", null=True)
    fechaHoraCreacion  = models.DateTimeField(auto_now_add=True,db_comment="Fecha y hora del registro")
    

    
class Contactanos(models.Model):
    conNombre = models.CharField(max_length=50, null=False, db_comment=" Nombre De La Persona Que Se Va Contactar")
    conEmail = models.CharField(max_length= 30, null=False,  db_comment="Direccion del correo electronico")
    conNumeroTe = models.IntegerField( null=True, db_comment="Telefono del usuario Que Se Contacta")
    conMensaje = models.CharField(max_length=150, null=True, db_comment="Mensaje Que El Usuario enviar para contartacnos")
    

Group.objects.get_or_create(name='Usuario')
Group.objects.get_or_create(name='Administrador')
Group.objects.get_or_create(name='Asistente')

