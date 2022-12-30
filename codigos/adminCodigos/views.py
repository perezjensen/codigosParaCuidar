from datetime import datetime
from django.shortcuts import render,HttpResponse,redirect
import pyqrcode
from perfilMascotas import models
from django.utils import timezone
from random import randint


# Create your views here.
def generar_Codigo(request):
    
    
    #generar una id unica para el codigo 
    codigoFecha=datetime.now()
    codigoFechaIso=codigoFecha.isoformat()
    numeroRandon= randint(1, 9999)
    codigoId=str(numeroRandon)+codigoFechaIso
  
    #obtengo la url actual 
    perfilId = request.build_absolute_uri(f'/perfil/{codigoId}')

   
    # Crea el código QR a partir de una cadena de texto
    qr = pyqrcode.create(perfilId,error='H')
    
    # Convierte el código QR a una imagen en formato PNG
    qr_png = qr.png_as_base64_str(scale=6)
    
    nuevoCodigo = models.PerfilMascotas()
    nuevoCodigo.idperfil=qr.data.decode()
    nuevoCodigo.save()
    

    
    # Renderiza la plantilla HTML con el código QR como una imagen
    return render(request, 'perfilMascotas/codigo.html', {'qr_code': qr_png})

def ver_codigos(request):
    # Obtiene todos los códigos QR de la tabla "codigos"
    codigos = models.PerfilMascotas.objects.all()
    # Crea una lista de imágenes PNG de los códigos QR
    codigos_png = []
    
    
    for codigo in codigos:
        qr = pyqrcode.create(codigo.idperfil)
        qr_png = qr.png_as_base64_str(scale=6)
       
        codigos_png.append(qr_png)
    
    # Renderiza la plantilla HTML con la lista de códigos QR en formato de imagen
    return render(request, 'perfilMascotas/ver_codigos.html', {'codigos_png': codigos_png})