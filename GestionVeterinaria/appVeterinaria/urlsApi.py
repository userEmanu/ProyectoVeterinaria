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
     path('PedidoList/',apiView.pedidoList.as_view()),
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
     path('PedidoList/<int:pk>/',apiView.pedidoDetail.as_view()),
     
     #login
     path('logout/',apiView.LogoutView.as_view()),
     path('login/',apiView.LoginView.as_view()),
     path('agregarMascotaApi/', apiView.aggMascotaView.as_view())
]