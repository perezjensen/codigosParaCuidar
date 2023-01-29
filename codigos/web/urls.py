from django.urls import path
from . import views



urlpatterns = [
    path('', views.landinPersonal, name='personal'),
    path('empresas/', views.landinEmpresas, name='empresas'),
  
  
]

