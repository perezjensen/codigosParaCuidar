from django.shortcuts import render,HttpResponse,redirect
from . import models

import requests


# Create your views here.
def ver_perfil(request,id):
    #obtengo la url actual 
    perfilId = request.build_absolute_uri(f'/perfil/{id}')
    
    
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if ip_address:
        # La solicitud ha sido redirigida a través de un servidor proxy
        # Se debe tomar en cuenta la primera dirección IP de la lista
        ip_address = ip_address.split(',')[0]
    else:
        # La solicitud no ha sido redirigida a través de un servidor proxy
        # Se puede obtener la dirección IP del cliente directamente
        ip_address = request.META['REMOTE_ADDR']
        
    return HttpResponse(ip_address)

    api_key = '75c1dec077ff4db7b4ac30cb7a55a8ac'
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_address}'
    response = requests.get(url)
    if response.status_code == 200:
        # La respuesta fue exitosa
        location_data = response.json()
        latitud = location_data['latitude']
        longitud = location_data['longitude']
        # Imprime la ubicación del usuario
        return redirect(f'https://www.google.com/maps?q={latitud},{longitud}')
    else:
        # La respuesta no fue exitosa
        return HttpResponse('no se encontro la direccion')
   

    
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


