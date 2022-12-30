from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class PerfilMascotas(models.Model):
    idperfil=models.CharField(max_length=500)
    nombreMascota=models.CharField(max_length=50,blank=True, null=True)
    telefono=models.CharField( max_length=50,blank=True, null=True)
    correo=models.EmailField(max_length=254,blank=True, null=True)
    nombreDueno=models.CharField(max_length=50,blank=True, null=True)
    created_date=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.idperfil