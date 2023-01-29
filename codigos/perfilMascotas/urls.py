from django.urls import path
from . import views



urlpatterns = [
    path('perfil/<id>', views.ver_perfil, name='perfil'),
    path('perfil/verificar/',views.verificarNombre,name='verificarNombre'),
    path('perfil/vacunas/guardar',views.guardarVacunas,name='guardarVacunas'),
    path('eliminarVacuna/<id>', views.eliminarVacuna, name='eliminarVacuna'),
    path('perfil/banos/guardar',views.guardarBanos,name='guardarBanos'),
    path('eliminarBano/<id>', views.eliminarBano, name='eliminarBano'),
    path('eliminarDesparasitante/<id>', views.eliminarDesparasitante, name='eliminarDesparasitante'),
    path('perfil/desparasitante/guardar',views.guardarDesparasitante,name='guardarDesparasitante'),
    path('eliminarPeso/<id>', views.eliminarPeso, name='eliminarPeso'),
    path('perfil/peso/guardar',views.guardarPeso,name='guardarPeso'),
    path('actualizar/',views.actualizarDatos,name='actualizarDatos'),
    path('picture/actualizar',views.actualizarImagen,name='actualizarImagen'),
    path('ubicacion/',views.ubicacion,name='ubicacion'),
    path('editar/nombre',views.editar,name='editar'),
]


