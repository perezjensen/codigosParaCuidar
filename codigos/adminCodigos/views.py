from django.shortcuts import render
import pyqrcode
from adminCodigos import models

# Create your views here.
def generar_Codigo(request):
    # Crea el código QR a partir de una cadena de texto
    qr = pyqrcode.create('https://www.facebook.com/stikerscolombia',error='H')
    
    # Convierte el código QR a una imagen en formato PNG
    qr_png = qr.png_as_base64_str(scale=6)
    
    nuevoCodigo = models.codigos()
    nuevoCodigo.codigo=qr.data.decode()
    nuevoCodigo.save()
    
    # Renderiza la plantilla HTML con el código QR como una imagen
    return render(request, 'perfilMascotas/codigo.html', {'qr_code': qr_png})

def ver_codigos(request):
    # Obtiene todos los códigos QR de la tabla "codigos"
    codigos = models.codigos.objects.all()
    
    # Crea una lista de imágenes PNG de los códigos QR
    codigos_png = []
    for codigo in codigos:
        qr = pyqrcode.create(codigo.codigo)
        qr_png = qr.png_as_base64_str(scale=6)
        codigos_png.append(qr_png)
    
    # Renderiza la plantilla HTML con la lista de códigos QR en formato de imagen
    return render(request, 'perfilMascotas/ver_codigos.html', {'codigos_png': codigos_png})