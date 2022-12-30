from django.urls import path
from . import views



urlpatterns = [
    path('codigo/', views.generar_Codigo, name='crearCodigo'),
    path('codigo/ver/', views.ver_codigos, name='verCodigo'),
]

