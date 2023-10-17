
from django.contrib import admin
from django.urls import path, include
from appVeterinaria import views
from django.conf.urls.static import static
from django.conf.urls import handler404 


from django.conf import settings

urlpatterns = [
    #urls de inicio Sesion o Inicio, que no han iniciado sesion
    path('admin/', admin.site.urls),
    path('',views.vistaInicio),
    path('inicio/',views.vistaInicio),
    path('nosotros/',views.vistaNosotrosInformacion),
    path('inicio/<str:mensaje>',views.vistaInicio),
    path('cerrarSesion/', views.CerrarSesion),
    path('vistaCodigo/', views.vistaCodigo),
    path('vistaRecuperarContra/', views.vistaRecuperarContra),
    path('vistaRegistrarse/',views.vistaRegistrarse),
    path('vistaConNueva/',views.vistConNueva),
    path('registrarseUser/', views.registrarseUsuario),
    path('iniciarSesion/',views.IniciarSesion),
    path('verificarCorreo/', views.VerificarCorreo),
    path('verificarCodigo/<int:id>', views.verificarCodigo),
    path('contraseñaNueva/<int:id>', views.RegistrarNuevaContraseña),
    path('registrarContactos/', views.registrarContactos),
    #----------------------------------------- 
    #urls sobre  Usuario
    #----------------------------------------- 
    path('vistaIndexUsuario/',views.vistaUsuario),
    path('vistaCitas/', views.vistaCitas),
    path('vistaServiciosTienda/', views.vistaServiciosTienda),
    path('vistaPerfilusuario/',views.vistaPerfilUsuario),
    path('vistaAgregarCita/<int:id>/', views.vistaAgregarCita),
    path('vistaAgregarCita/<int:id>/<str:mensaje>/', views.vistaAgregarCita),
    path('agregarCita/<int:id>/', views.agregarCita),
    path('detPedidoUser/<int:id>/', views.detallePedido),
    path('subirImagenComprobante/<int:id>/', views.cargarImagenComprobantePedido),
    path('agregarMacota/', views.AgregarMascota),
    path('subirImagenPerfil/<int:id>/', views.subirImagenPerfilUser),
    path('actualizarDatosPerfil/<int:id>/', views.actualizarDatosUsuario),
    path('cancelarPedidoUser/<int:id>/', views.cancelarPedidoUser),
    #----------------------------------------- 
    #urls sobre Tienda de los productos para comprar
    #----------------------------------------- 
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('vistaTienda/', views.vistaTienda, name="tienda"),
    path('vistaTiendaPromociones/', views.vistaTiendaPromociones),
    path('vistaTiendaCategoria/<int:id>/', views.vistaTiendaCategoria),
    path('detalleDerServicio/<int:id>/', views.vistaServiciosTiendaDescripcion),
    path('buscarProveedor/<int:id>/', views.vistaTiendaMarcas),
    path('vistaCarrito/', views.vistaCarrito, name="carrito"),
    path('detalle/<int:id>/', views.vistaDetalleProducto, name='detalle_producto'),
    path('finalizarCompra/', views.finalizar_compra),
    path('finalizarCompra/<str:mensaje>/', views.finalizar_compra),
    path('procesarPedido/', views.procesar_pedido),
    path('agregar/<int:id>/', views.agregar_producto, name="Agregar"),
    path('eliminar/<int:id>/', views.eliminar_producto, name="Eliminar"),
    path('restar/<int:id>/', views.restar_producto, name="Restar"),
    path('limpiar/', views.limpiar_carrito, name="Limpiar"),
    #----------------------------------------- 
    #Funciones del administrado y vistas
    #----------------------------------------- 
    path('vistaAdministrador/',views.vistaAdministrador),
    path('perfiladmin/',views.perfiladmin),
    path('AgregarEmpleado/',views.vistaAgregarEmpleado),
    path('VistaAgregarEmpleado/',views.VistaAgregarEmpleado),
    path('VistaProductos/', views.VistaProductos),
    path('editar_producto/<int:id>/', views.editar_producto, name='editar_producto'),
    path('elimina/<int:id>/', views.eliminar_product, name='eliminar'),  
    path('RegistrarProducto/', views.RegistrarProducto),
    path('vistaEmpleadoUsuario/<int:id>',views.vistaEmpleadoUsuario), 
    path("listarUsuarios/", views.vistasListarUsuarios),
    path('GestionServicio/',views.vistaGestionServicio),
    path('gestionCitas/', views.vistaGestionCitas),
    path("descripcionCita/<int:id>", views.vistaCitaHTML),
    path("realizarCita/<int:id>", views.citaRealizada),
    path('cancelarCita/<int:id>/', views.cancelarCita),
    path('RegistrarProveedor/', views.VistaRegistrarProveedor),
    path('RegistrarCategoria/', views.VistaRegistrarCategoria),
    path('registrarEmpleadoUser/<int:id>/', views.CrearUsuarioEmpleado),
    path("agregarServicio/",views.agregarServicio),
    path('asignarservicio/',views.asignasServicio),
    path('generarPDFHistorialEnviar/<int:id>/', views.descargarPDFhistorial),
    path('cambiarEstadoPedido/<int:id>/', views.cambiarestadoPedido),
    path('gestionPedidos/', views.vistaGestionPedidos),
    path('suspenderUser/<int:id>/<str:mensaje>/', views.Suspende_Activar_Usuario),
    path('editarServicioAdminInfo/<int:id>/', views.mostrarEditarServicio),
    path('editarServicioAdmin/<int:id>/', views.editaSersvicioAdministradro),
    path('ventasPorBimestral/', views.datosBimestralesAnuales),
    path('recordatoriosDeLasCitasTodas/', views.enviarCorreosDeRecordatorioAtodas),
    path('recordatoriosDeLasCitasPersonalizada/<int:id>/', views.recordatorioDeCitaPersonalizado),
    path('responderContact/<int:id>/', views.responderMensajeCOntactanos),
    path('detalleCitaMascota/<int:id>/', views.detalleDeLaCitaMascota),
    #----------------------------------------- 
    #API todo sobre api
    path('', include('appVeterinaria.urlsApi'))
]

if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    

