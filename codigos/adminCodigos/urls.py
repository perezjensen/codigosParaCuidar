from django.urls import path
from . import views



urlpatterns = [
    path('codigo/', views.generar_Codigo, name='crearCodigo'),
    path('codigo/ver/', views.ver_codigos, name='verCodigo'),
    path('codigoAdmin/', views.codigoAdmin, name='codigoAdmin'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/guardar', views.guardarCliente, name='guardarCliente'),
    path('clientes/editar/<id>', views.editarCliente, name='editarCliente'),
    path('imprimir/<cliente>', views.imprimirRecientes, name='imprimirRecientes'),
    path('verCodigos/<id>', views.verCodigosCliente, name='verCodigosCliente'),
    path('imprimir/', views.imprimir, name='imprimir'),
    path('eliminarCodigo/<idcodigo>/<id>', views.eliminarCodigo, name='eliminarCodigo'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='cerrar'),
    path('codigo/cliente/<id>', views.VerFormclienteCodigo, name='codigoCliente'),
    path('cliente/eliminar/<id>', views.eliminarCliente, name='eliminarCliente'),
]

