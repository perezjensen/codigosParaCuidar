from django.urls import path
from . import views



urlpatterns = [
    path('', views.ver_perfil, name='perfil'),
   
]

