from django.urls import path
from . import views



urlpatterns = [
    path('perfil/<id>', views.ver_perfil, name='perfil'),
   
]

