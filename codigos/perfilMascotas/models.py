from django.db import models
from django.conf import settings
from django.utils import timezone
from adminCodigos.models import Cliente
from web.models import Pais
# Create your models here.



    
class PerfilMascotas(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idperfil=models.CharField(max_length=500)
    nombreMascota=models.CharField(max_length=50,blank=True, null=True)
    telefono=models.CharField( max_length=50,blank=True, null=True)
    correo=models.EmailField(max_length=254,blank=True, null=True)
    nombreDueno=models.CharField(max_length=50,blank=True, null=True)
    created_date=models.DateTimeField(default=timezone.now)
    imagenPerfil=models.ImageField(upload_to='perfiles',null=True,blank=True)
    raza=models.CharField(max_length=50,blank=True, null=True)
    edad=models.IntegerField(blank=True, null=True)
    recompensa=models.FloatField(max_length=50,blank=True, null=True)
    esterilizacion=models.CharField(max_length=50,blank=True, null=True)
    sexo=models.CharField(max_length=50,blank=True, null=True)
    precio=models.FloatField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    pais=models.ForeignKey(Pais, on_delete=models.CASCADE, null=True, blank=True, default=None)

    
    
    
    def __str__(self):
        return self.idperfil
    
class vacuna(models.Model):
    mascota = models.ForeignKey(PerfilMascotas, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    vacuna=models.CharField( max_length=50)
    dosis=models.CharField( max_length=50)
    
class bano(models.Model):
    mascota = models.ForeignKey(PerfilMascotas, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    descripcion=models.CharField( max_length=300)
    
class desparasitante(models.Model):
    mascota = models.ForeignKey(PerfilMascotas, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    antiparasitario=models.CharField( max_length=50)
    dosis=models.CharField( max_length=50)

class peso(models.Model):
    mascota = models.ForeignKey(PerfilMascotas, on_delete=models.CASCADE)
    fecha=models.DateTimeField()
    peso=models.CharField( max_length=50)

