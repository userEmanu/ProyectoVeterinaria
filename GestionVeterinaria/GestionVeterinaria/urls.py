"""
URL configuration for GestionVeterinaria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from appVeterinaria import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('e/',views.vistaInicio),
    path('inicio/',views.vistaInicio),
    path('cerrarSesion/', views.CerrarSesion),
    path('vistaCitas/', views.vistaCitas),
    path('vistaCodigo/', views.vistaCodigo),
    path('vistaProductos/', views.vistaproductos, name="productos"),
    path('vistaAdministrador/',views.vistaAdministrador),
    path('perfiladmin/',views.perfiladmin),
    path('AgregarEmpleado/',views.vistaAgregarEmpleado),
    path('VistaAgregarEmpleado/',views.VistaAgregarEmpleado),
    path('listarEmpleados/',views.listarEmpleados),
    path('VistaProductos/', views.VistaProductos),
    path('RegistrarProducto/', views.RegistrarProducto),
    path('vistaPerfilusuario/',views.vistaPerfilUsuario),
    path('vistaIndexUsuario/',views.vistaUsuario),
    path('vistaRecuperarContra/', views.vistaRecuperarContra),
    path('vistaRegistrarse/',views.vistaRegistrarse),
    path('vistaConNueva/',views.vistConNueva),
    path('vistaEmpleadoUsuario/<int:id>',views.vistaEmpleadoUsuario), 
    path('GestionServicio/',views.vistaGestionServicio),
    path('gestionCitas/', views.vistaGestionCitas),
    path("", views.vistaCita),
    
    #----------------------------------------- 
    path('cancelarCita/<int:id>', views.cancelarCita),
    path('registrarseUser/', views.registrarseUsuario),
    path('iniciarSesion/',views.IniciarSesion),
    path('verificarCorreo/', views.VerificarCorreo),
    path('RegistrarProveedor/', views.VistaRegistrarProveedor),
    path('RegistrarCategoria/', views.VistaRegistrarCategoria),
    path('verificarCodigo/<int:id>', views.verificarCodigo),
    path('contraseñaNueva/<int:id>', views.RegistrarNuevaContraseña),
    path('registrarContactos/', views.registrarContactos),
    path('agregar/<int:id>/', views.agregar_producto, name="Add"),
    path('eliminar/<int:id>/', views.eliminar_producto, name="Del"),
    path('restar/<int:id>/', views.restar_producto, name="Sub"),
    path('limpiar/', views.limpiar_carrito, name="CLS"),
    path('registrarEmpleadoUser/<int:id>/', views.CrearUsuarioEmpleado),
    path("agregarServicio/",views.agregarServicio),
    path('vistaAgregarCita/<int:id>/', views.vistaAgregarCita),
    path('vistaAgregarCita/<int:id>/<str:mensaje>/', views.vistaAgregarCita),
    path('agregarCita/<int:id>/', views.agregarCita),
    path('asignarservicio/',views.asignasServicio),
    
    
    
    path('', include('appVeterinaria.urlsApi')),
]



if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
