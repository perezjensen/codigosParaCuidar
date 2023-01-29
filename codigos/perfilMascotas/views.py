from django.shortcuts import render,HttpResponse,redirect
from . import models
import requests
from django.urls import reverse
from PIL import Image
from django.contrib import messages
from .forms import CreatePerfil,CreateVacunas, CreateBano, CreateDesparasitante,CreatePeso,UdpdatePerfil,UpdateImage

from PIL import Image
from io import BytesIO
from django.core.files import File
import json
from django.views.defaults import page_not_found
import re

import smtplib, ssl
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.mail import send_mail

from django.template.loader import render_to_string

def mostrar_perfil(request,origen):
    
    buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
    
    vacunasMostrar=models.vacuna.objects.filter(mascota=buscarPerfil)
    banosMostrar=models.bano.objects.filter(mascota=buscarPerfil)
    desparasitanteMostrar=models.desparasitante.objects.filter(mascota=buscarPerfil)
    pesoMostrar=models.peso.objects.filter(mascota=buscarPerfil)
    
    if origen == 'banos':
        formBanos= CreateBano(request.POST)
        form = CreateVacunas()
        formdesparasitante=CreateDesparasitante()
        formPeso=CreatePeso()
        formDatosMascota=UdpdatePerfil()
        formUpdateImagen = UpdateImage()
        
    elif origen == 'vacuna':
        form = CreateVacunas(request.POST)
        formBanos= CreateBano()
        formdesparasitante=CreateDesparasitante()
        formPeso=CreatePeso()
        formDatosMascota=UdpdatePerfil()
        formUpdateImagen = UpdateImage()
    
    elif origen =='desparasitante':
        formdesparasitante=CreateDesparasitante(request.POST)
        formBanos= CreateBano()
        form = CreateVacunas()
        formPeso=CreatePeso()
        formDatosMascota=UdpdatePerfil()
        formUpdateImagen = UpdateImage()
        
    elif origen =='peso':
        formdesparasitante=CreateDesparasitante()
        formBanos= CreateBano()
        form = CreateVacunas()
        formPeso=CreatePeso(request.POST)
        formDatosMascota=UdpdatePerfil()
        formUpdateImagen = UpdateImage()
        
    elif origen =='actualizar':
        formdesparasitante=CreateDesparasitante()
        formBanos= CreateBano()
        form = CreateVacunas()
        formPeso=CreatePeso()
        formDatosMascota=UdpdatePerfil(request.POST)
        formUpdateImagen = UpdateImage()
    
    elif origen == 'actualizarImagen':
        formdesparasitante=CreateDesparasitante()
        formBanos= CreateBano()
        form = CreateVacunas()
        formPeso=CreatePeso()
        formDatosMascota=UdpdatePerfil()
        formUpdateImagen = UpdateImage(request.POST, request.FILES)
        
        
    else:
        formdesparasitante=CreateDesparasitante()
        formBanos= CreateBano()
        form = CreateVacunas()
        formPeso=CreatePeso()
        formDatosMascota=UdpdatePerfil()
        formUpdateImagen = UpdateImage()
 
    
    return render(request, 'perfilMascotas/admin.html',{
                                                        'datos':buscarPerfil,
                                                        'form':form,
                                                        'formBanos':formBanos,
                                                        'vacunasMostrar':vacunasMostrar,
                                                        'banosMostrar':banosMostrar,
                                                        'desparasitanteMostrar':desparasitanteMostrar,
                                                        'formdesparasitante':formdesparasitante,
                                                        'formPeso':formPeso,
                                                        'pesoMostrar':pesoMostrar,
                                                        'formDatosMascota':formDatosMascota,
                                                        'formUpdateImagen': formUpdateImagen,
                                                        'id':request.session['solo_id'],
                                                        
                                                          })



def ver_perfil(request,id):
    #obtengo la url actual 
    request.session['solo_id'] = id
    perfilId = request.build_absolute_uri(f'/perfil/{id}')
    #guardo en seccion 
    request.session['id_perfil'] = perfilId
   

    try:
        # Se busca el perfil en la base de datos utilizando el id del perfil
        buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
        
        if buscarPerfil.nombreDueno:
            # El nombre del dueño tiene datos, entonces se obtienen las vacunas, banos, desparasitantes y pesos relacionados con la mascota
            vacunasMostrar=models.vacuna.objects.filter(mascota=buscarPerfil)
            banosMostrar=models.bano.objects.filter(mascota=buscarPerfil)
            desparasitanteMostrar=models.desparasitante.objects.filter(mascota=buscarPerfil)
            pesoMostrar=models.peso.objects.filter(mascota=buscarPerfil)
            url = reverse('ubicacion')
            return render(request, 'perfilMascotas/perfil.html',{'datos':buscarPerfil,
                                                                 'id': request.session['id_perfil'],
                                                                 'vacunasMostrar':vacunasMostrar,
                                                                 'banosMostrar':banosMostrar,
                                                                 'desparasitanteMostrar':desparasitanteMostrar,
                                                                 'pesoMostrar':pesoMostrar,
                                                                 'url': url,
                                                                 }
                          )
        else:
            
            if request.method=="POST":
                
                # se valida el formulario
                form = CreatePerfil(request.POST, request.FILES)
            
           
                if form.is_valid(): 
                    numero= form.cleaned_data.get('telefono')
                    paisform=form.cleaned_data.get('pais')
                    
                    pais = re.sub(r'\D', '', str(paisform))
                    telefono=str(pais)+str(numero)
                  
                    # Obtén la imagen del formulario
                    logo = form.cleaned_data.get('imagenPerfil')
                    # Abre la imagen original
                    im = Image.open(logo)
                    # Redimensiona la imagen
                    im.thumbnail((500, 500))
                    # Convierte la imagen redimensionada a un objeto "File"
                    logo_thumbnail = BytesIO()
                    im.save(logo_thumbnail, format='PNG')
                    logo_thumbnail.seek(0)
                    # Crea una nueva instancia de la tabla Logo con la imagen redimensionada
                    imagen=File(logo_thumbnail, name=f'logo.png')
                    buscarPerfil.nombreMascota = form.cleaned_data.get('nombreMascota')
                    buscarPerfil.telefono = telefono
                    buscarPerfil.correo = form.cleaned_data.get('correo')
                    buscarPerfil.nombreDueno=form.cleaned_data.get('nombreDueno')
                    buscarPerfil.imagenPerfil=imagen
                    buscarPerfil.pais=form.cleaned_data.get('pais')
                    buscarPerfil.esterilizacion='no aplica'
                    buscarPerfil.save()
                    return render(request, 'perfilMascotas/perfil.html',{'datos':buscarPerfil})
                
                else:
                    return render(request, 'perfilMascotas/activar.html', {'form': form, 'id': request.session['id_perfil'],'foto':buscarPerfil})
                
            form = CreatePerfil()
            
            return render(request, 'perfilMascotas/activar.html',{'form':form,'id':request.session['id_perfil'],'foto':buscarPerfil})

    except models.PerfilMascotas.DoesNotExist:
        # En este caso, el perfil no existe en la base de datos
        return render(request, 'perfilMascotas/404.html')

    

def verificarNombre(request):
    if request.method=="POST":
        nombre = request.POST['nombre']
        buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
        
        if buscarPerfil.nombreDueno.lower()==nombre.lower():
            return mostrar_perfil(request,origen="verificarNombre")
        else:
            messages.error(request, 'Tu nombre no coincide, Intenta de nuevo')
            
            return redirect('editar')


    else:
        return render(request, 'perfilMascotas/404.html')
       
    


def guardarVacunas(request):
    if request.method=="POST":  
        vacuna = models.vacuna()   
        buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
        form = CreateVacunas(request.POST)
        
        
        if form.is_valid():
            vacuna.mascota=buscarPerfil
            vacuna.fecha = form.cleaned_data.get('fecha')
            vacuna.vacuna = form.cleaned_data.get('vacuna')
            vacuna.dosis = form.cleaned_data.get('dosis')
            vacuna.save()
            return mostrar_perfil(request,origen="vacunasTrue")
        else:
            return mostrar_perfil(request,origen="vacuna")
    else:
         return render(request, 'perfilMascotas/404.html')
        
def eliminarVacuna(request,id):
    # Eliminar el registro con la id especificada
    vacuna=models.vacuna.objects.get(id=id)
    vacuna.delete()
    return mostrar_perfil(request,origen="eliminarvacuna")
        
def guardarBanos(request):
    if request.method=="POST":
        formBanos = CreateBano(request.POST)
        if formBanos.is_valid():
            bano= models.bano()
            bano.fecha = formBanos.cleaned_data.get('fecha')
            bano.descripcion = formBanos.cleaned_data.get('descripcion')
            buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
            bano.mascota= buscarPerfil
            bano.save()
            return mostrar_perfil(request,origen="banosTrue")
            
        else:
            return mostrar_perfil(request,origen="banos")
    else:
        return render(request, 'perfilMascotas/404.html')
        
        
def eliminarBano(request,id):
    # Eliminar el registro con la id especificada
    bano=models.bano.objects.get(id=id)
    bano.delete()
    return mostrar_perfil(request,origen="eliminarbaño")

def  eliminarDesparasitante(request,id):
    # Eliminar el registro con la id especificada
    desparasitante=models.desparasitante.objects.get(id=id)
    desparasitante.delete()
    return mostrar_perfil(request,origen="eliminardesparasitante")

def guardarDesparasitante(request):
    if request.method=="POST":
        formdesparasitante = CreateDesparasitante(request.POST)
        if formdesparasitante.is_valid():
            desparasitante= models.desparasitante()
            desparasitante.fecha = formdesparasitante.cleaned_data.get('fecha')
            desparasitante.antiparasitario = formdesparasitante.cleaned_data.get('antiparasitario')
            desparasitante.dosis=formdesparasitante.cleaned_data.get('dosis')
            buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
            desparasitante.mascota= buscarPerfil
            desparasitante.save()
            return mostrar_perfil(request,origen="desparasitanteTrue")
            
        else:
            return mostrar_perfil(request,origen="desparasitante")
    else:
        return render(request, 'perfilMascotas/404.html')
        
        
def eliminarPeso(request,id):
    # Eliminar el registro con la id especificada
    peso=models.peso.objects.get(id=id)
    peso.delete()
    return mostrar_perfil(request,origen="eliminarpeso")

def guardarPeso(request):
    if request.method=="POST":
        formPeso = CreatePeso(request.POST)
        if formPeso.is_valid():
            peso= models.peso()
            peso.fecha = formPeso.cleaned_data.get('fecha')
            peso.peso = formPeso.cleaned_data.get('peso')

            buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
            peso.mascota= buscarPerfil
            peso.save()
            return mostrar_perfil(request,origen="pesoTrue")
            
        else:
            return mostrar_perfil(request,origen="peso")
    else:
        return render(request, 'perfilMascotas/404.html')
        
def actualizarDatos(request):
    
    if request.method=="POST":
        
        formDatosMascota = UdpdatePerfil(request.POST)
        
        if formDatosMascota.is_valid():
            buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
            
            buscarPerfil.nombreMascota = formDatosMascota.cleaned_data.get('nombreMascota')
            buscarPerfil.raza = formDatosMascota.cleaned_data.get('raza')
            

                
            if formDatosMascota.cleaned_data.get('edad'):
                buscarPerfil.edad = formDatosMascota.cleaned_data.get('edad')
                
            if formDatosMascota.cleaned_data.get('sexo'):
                buscarPerfil.sexo = formDatosMascota.cleaned_data.get('sexo')
            
            if formDatosMascota.cleaned_data.get('telefono'):
                buscarPerfil.telefono = formDatosMascota.cleaned_data.get('telefono')
                
                
            if formDatosMascota.cleaned_data.get('correo'):    
                buscarPerfil.correo = formDatosMascota.cleaned_data.get('correo')
            
            if formDatosMascota.cleaned_data.get('observaciones'):
                buscarPerfil.observaciones=formDatosMascota.cleaned_data.get('observaciones')

            if formDatosMascota.cleaned_data.get('recompensa'):
                    buscarPerfil.recompensa = formDatosMascota.cleaned_data.get('recompensa')
                    
            buscarPerfil.esterilizacion = formDatosMascota.cleaned_data.get('esterilizacion')  
            
            buscarPerfil.save()
            return mostrar_perfil(request,origen="actualizarTrue")
            
        else:
            return mostrar_perfil(request,origen="actualizar")
    else:
        return render(request, 'perfilMascotas/404.html')
        
        


def actualizarImagen(request):
    formUpdateImagen = UpdateImage(request.POST, request.FILES)
    if formUpdateImagen.is_valid():
        buscarPerfil = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil'])
        try:
            buscarPerfil.imagenPerfil.delete()
        except ValueError:
            pass
        
        # Obtén la imagen del formulario
        logo = formUpdateImagen.cleaned_data.get('imagenPerfil')
        # Abre la imagen original
        im = Image.open(logo)
        # Redimensiona la imagen
        im.thumbnail((500, 500))
        # Convierte la imagen a formato RGB
           
        # Convierte la imagen redimensionada a un objeto "File"
        logo_thumbnail = BytesIO()
        im.save(logo_thumbnail, format='PNG')
        logo_thumbnail.seek(0)

            
        # Crea una nueva instancia de la tabla Logo con la imagen redimensionada
        imagen=File(logo_thumbnail, name=f'logo.png')
        
        buscarPerfil.imagenPerfil=imagen
        buscarPerfil.save()
        return mostrar_perfil(request,origen="actualizarImagenTrue")
    else:
        return mostrar_perfil(request,origen="actualizarImagen")
    
    





def editar(request):
    return render(request, 'perfilMascotas/editar.html')



        


def ubicacion(request):
  
    if request.method == 'POST':
        data = json.loads(request.body)
        latitud = data['latitud']
        longitud = data['longitud']
        url=f'https://www.google.com/maps/search/?api=1&query={latitud},{longitud}'
        subject= 'Alerta de Ubicacion de Mascota'
        correo = models.PerfilMascotas.objects.get(idperfil=request.session['id_perfil']).correo
        email_from = settings.EMAIL_HOST_USER
        recipient_list=[correo]
        
        message = render_to_string('perfilMascotas/correo.html', { 'url': url})
        send_mail(subject, message, email_from, recipient_list, html_message=message)

        return JsonResponse({'status': 'success'})

        
    return JsonResponse({'status': 'error'})
