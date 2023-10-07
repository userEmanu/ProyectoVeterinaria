from django.urls import path
from . import apiView

urlpatterns = [
     path('UserList/',apiView.userList.as_view()),
     path('EmpleadoList/',apiView.empleadoList.as_view()),
     path('DetalleEnvioList/',apiView.detalleEnvioList.as_view()),
     path('ProveedorList/',apiView.proveedorList.as_view()),
     path('CategoriaList/',apiView.categoriaList.as_view()),
     path('MascotaList/',apiView.mascotaList.as_view()),
     path('CitaList/',apiView.citaList.as_view()),
     path('ProductorList/',apiView.productoList.as_view()),
     path('DetallePedidoList/',apiView.detallePedidoList.as_view()),

     # listas Id
     path('UserList/<int:pk>/',apiView.userDetail.as_view()),
     path('EmpleadoList/<int:pk>/',apiView.empleadoDetail.as_view()),
     path('DetalleEnvioList/<int:pk>/',apiView.detalleEnvioDetail.as_view()),
     path('ProveedorList/<int:pk>/',apiView.proveedorDetail.as_view()),
     path('CategoriaList/<int:pk>/',apiView.categoriaDetail.as_view()),
     path('MascotaList/<int:pk>/',apiView.mascotaDetail.as_view()),
     path('CitaList/<int:pk>/',apiView.citaDetail.as_view()),
     path('ProductorList/<int:pk>/',apiView.productoDetail.as_view()),
     path('DetallePedidoList/<int:pk>/',apiView.detallePedidoDetail.as_view()),

     path('buscar_mascota/<int:id>/', apiView.mascotaBuscar.as_view()),
     path('buscar_citas/<int:id>/', apiView.CitasUsuarioApi.as_view()),
     path("buscar_pedidos/<int:id>/",apiView.PedidosUsuarioAPI.as_view()),
     path("listarServicios/",apiView.serviciosListarapi.as_view()),
     
     
     #login
     path('logout/',apiView.LogoutView.as_view()),
     path('login/',apiView.LoginView.as_view()),
     path('agregarMascotaApi/', apiView.aggMascotaView.as_view()),
     path('productoImagen/', apiView.ProductoImagen.as_view()),
     path('mascotaImagen/', apiView.MascotaFoto.as_view()),
     path('UsuarioImagen/', apiView.userFoto.as_view()),
     path('editarUsuario/', apiView.editarUsuarioView.as_view()),
     path('todoLosProductos/', apiView.productosTodos.as_view()),
     path('agregarcitaApi/', apiView.AgregarCitaAPI.as_view()),
     path('informacionAdministrador/', apiView.informacionAdministrador.as_view()),
     path('informacionAdministradorPedidosHoy/', apiView.informacionAdministradorGraficas.as_view()),
     path('informacionAdministradorPedidos/', apiView.informacionAdministradorPedidos.as_view()),
     path('informacionAdministradorCitas/', apiView.informacionAdministradorCitas.as_view()),
     path('informacionAdministradorGanancias/', apiView.informacionAdministradorGanancias.as_view()),
     path('pedidoRegistrarApi/', apiView.AgregarPedidoApiRest.as_view()),
]