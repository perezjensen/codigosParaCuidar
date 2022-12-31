from django.shortcuts import render,HttpResponse,redirect
from . import models
import requests


# Create your views here.
def ver_perfil(request,id):
    #obtengo la url actual 
    perfilId = request.build_absolute_uri(f'/perfil/{id}')

    try:
        buscarPerfil = models.PerfilMascotas.objects.get(idperfil=perfilId)
        
        if buscarPerfil.nombreDueno:
            # El nombre del dueño tiene datos, entonces los muestra
            return HttpResponse('muestra datos')
        else:
            return HttpResponse('sin datos')
            
        
    except models.PerfilMascotas.DoesNotExist:
        # En este caso, el perfil no existe en la base de datos
        return HttpResponse('no')
    

    
    return render(request, 'perfilMascotas/perfil.html', {})


