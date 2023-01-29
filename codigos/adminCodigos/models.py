from django.db import models

from web.models import Pais

# Create your models here.
from django.conf import settings
from django.utils import timezone
# Create your models here.

class codigos(models.Model):
    #user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    codigo=models.CharField(max_length=500, null=False, default=None)
    created_date=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.codigo
    
    
class Cliente(models.Model):
    nombreNegocio=models.CharField(max_length=500)
    nombreCliente=models.CharField(max_length=500, null=False, default=None)
    correo=models.EmailField(max_length=254,null=False, default=None)
    logo = models.ImageField(upload_to='logos',null=False, default=None)
    direccion=models.CharField(max_length=500, null=False, default=None)
    ciudad=models.CharField(max_length=50, null=False, default=None)
    telefono=models.CharField(max_length=30, null=False, default=None)
    observaciones = models.TextField(blank=True, null=True)
    tictok=models.CharField(max_length=50,blank=True, null=True)
    facebook=models.CharField(max_length=50,blank=True, null=True)
    instagram=models.CharField(max_length=50,blank=True, null=True)
    created_date=models.DateTimeField(default=timezone.now)
    pais=models.ForeignKey(Pais, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.nombreNegocio
    


