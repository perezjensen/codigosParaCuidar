from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class PerfilMascotas(models.Model):
    nombreMascota=models.CharField(max_length=50)
    telefono=models.CharField( max_length=50)
    correo=models.EmailField(max_length=254)
    nombreDueno=models.CharField(max_length=50)
    created_date=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.nombreMascota