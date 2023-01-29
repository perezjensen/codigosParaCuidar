from datetime import datetime
from django.shortcuts import render,HttpResponse,redirect
import pyqrcode
from perfilMascotas import models
from django.utils import timezone
from random import randint
from .forms import ClienteForm,GenerarCodigo,EditarClienteForm
from datetime import datetime, time
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django_filters import FilterSet, DateFilter
import base64
import io
import os
from django.conf import settings
from django.core.files import File
import re
from django.contrib.auth.forms import UserCreationForm

from django.db.models import  Count
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
@login_required
def generar_Codigo(request):
    
    if request.method=="POST":
        formCodigo=GenerarCodigo(request.POST)
        if formCodigo.is_valid():
            cliente_id = request.POST.get('cliente')
            cantidad = request.POST['cantidad']
            
            
            if request.POST.get('grupal'):
                precio=float(request.POST['precio'])/int(cantidad)
                
            else:
                precio= formCodigo.cleaned_data['precio']
                
            
            for I in range(int(cantidad)):
                #generar una id unica para el codigo 
                codigoFecha=datetime.now()
                codigoFechaIso=codigoFecha.isoformat()
                numeroRandon= randint(1, 9999)
                codigoId=str(numeroRandon)+codigoFechaIso
                #obtengo la url actual 
                perfilId = request.build_absolute_uri(f'/perfil/{codigoId}')
                
                cliente=formCodigo.cleaned_data['cliente']
                nuevoCodigo = models.PerfilMascotas()
                nuevoCodigo.idperfil=perfilId
                nuevoCodigo.cliente=formCodigo.cleaned_data['cliente']
                nuevoCodigo.precio=precio
                nuevoCodigo.save()
                
            formCodigo=GenerarCodigo(request.POST)
            dateNow = datetime.now()
            dateNow_min = datetime.combine(dateNow, time.min)
            dateNow_max = datetime.combine(dateNow, time.max)
            
            codigo=models.PerfilMascotas.objects.filter(created_date__range=(dateNow_min, dateNow_max)).filter(cliente=cliente)
            
      
            
            return render(request, 'adminCodigos/generarCodigo.html',{'formCodigo':formCodigo,'codigos':codigo,'cliente':cliente_id })
        else:
            return redirect('codigoAdmin') 
    else:
        return redirect('codigoAdmin')   
    
@login_required  
def VerFormclienteCodigo(request,id):
    formCodigo=GenerarCodigo()
    
    return render(request,'adminCodigos/codigoClienteGenerar.html',{'formCodigo':formCodigo,'cliente':id})

@login_required
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

@login_required
def codigoAdmin(request):
    formCodigo=GenerarCodigo(request.POST, request.FILES)
    return render(request, 'adminCodigos/generarCodigo.html',{'formCodigo':formCodigo })
    
@login_required
def clientes(request):
    
    cliente = models.Cliente.objects.annotate(num_perfiles_mascota=Count('perfilmascotas__id'))
    return render(request, 'adminCodigos/clientes.html',{'clientes':cliente })
    
@login_required   
def guardarCliente(request):
    if request.method=="POST":
        formCliente=ClienteForm(request.POST,request.FILES)
        if formCliente.is_valid():
            # Obtén la imagen del formulario
            logo = formCliente.cleaned_data['logo']
            # Abre la imagen original
            im = Image.open(logo)
            # Redimensiona la imagen
            im.thumbnail((300, 300))
            # Convierte la imagen a formato RGB
            # Convierte la imagen redimensionada a un objeto "File"
            logo_thumbnail = BytesIO()
            im.save(logo_thumbnail, format='PNG')
            logo_thumbnail.seek(0)
            paisform=formCliente.cleaned_data.get('pais')
            numero=formCliente.cleaned_data['telefono']         
            pais = re.sub(r'\D', '', str(paisform))
            telefono=str(pais)+str(numero)

            # Crea una nueva instancia de la tabla Logo con la imagen redimensionada
            imagen=File(logo_thumbnail, name=f'logo.png')
            cliente = models.Cliente()
            cliente.nombreCliente = formCliente.cleaned_data['nombreCliente']
            cliente.nombreNegocio = formCliente.cleaned_data['nombreNegocio']
            cliente.correo = formCliente.cleaned_data['correo']
            cliente.direccion = formCliente.cleaned_data['direccion']
            cliente.observaciones = formCliente.cleaned_data['observaciones']
            cliente.ciudad = formCliente.cleaned_data['ciudad']
            cliente.facebook=formCliente.cleaned_data['facebook']
            cliente.instagram=formCliente.cleaned_data['instagram']
            cliente.tictok=formCliente.cleaned_data['tictok']
            cliente.telefono = telefono
            cliente.pais=formCliente.cleaned_data['pais']
            cliente.logo= imagen
            cliente.save()
            
            
            cliente = models.Cliente.objects.annotate(num_perfiles_mascota=Count('perfilmascotas__id'))
            return render(request, 'adminCodigos/clientes.html',{'clientes':cliente })
        else:
            formCliente=ClienteForm(request.POST,request.FILES)
            cliente = models.Cliente.objects.all()
            return render(request, 'adminCodigos/registrarCliente.html',{'formCliente':formCliente })
    else:
        formCliente=ClienteForm()
        cliente = models.Cliente.objects.all()
        return render(request, 'adminCodigos/registrarCliente.html',{'formCliente':formCliente })
        
    
    
    
    
@login_required   
def editarCliente(request,id):
    cliente=models.Cliente.objects.get(pk=id)
    formCliente=EditarClienteForm(request.POST,request.FILES)
    if request.method=="POST":
        if formCliente.is_valid():
            
            
            if request.FILES.get('logo'):
                # Obtén la imagen del formulario
                logo = request.FILES.get('logo')
                # Abre la imagen original
                im = Image.open(logo)
                # Redimensiona la imagen
                im.thumbnail((300, 300))
                # Convierte la imagen a formato RGB
                # Convierte la imagen redimensionada a un objeto "File"
                logo_thumbnail = BytesIO()
                im.save(logo_thumbnail, format='PNG')
                logo_thumbnail.seek(0)
                # Crea una nueva instancia de la tabla Logo con la imagen redimensionada
                imagen=File(logo_thumbnail, name=f'logo.png')
                cliente.logo = imagen
                
                                
            
            cliente.nombreCliente = formCliente.cleaned_data['nombreCliente']
            cliente.nombreNegocio = formCliente.cleaned_data['nombreNegocio']
            cliente.correo = formCliente.cleaned_data['correo']
            cliente.direccion = formCliente.cleaned_data['direccion']
            cliente.ciudad = formCliente.cleaned_data['ciudad']
            cliente.telefono = formCliente.cleaned_data['telefono']
            cliente.facebook=formCliente.cleaned_data['facebook']
            cliente.tictok=formCliente.cleaned_data['tictok']
            cliente.instagram=formCliente.cleaned_data['instagram']
            cliente.observaciones=formCliente.cleaned_data['observaciones']
            
            cliente.save()
            
            
            cliente = models.Cliente.objects.all()
            return render(request, 'adminCodigos/clientes.html',{'clientes':cliente })
        
    
    return render(request, 'adminCodigos/clientesEditar.html',{'formCliente':formCliente,'cliente':cliente })




class PerfilMascotasFilter(FilterSet):
    created_date = DateFilter(field_name='created_date', lookup_expr='exact')

    class Meta:
        model = models.PerfilMascotas
        fields = ['created_date']

@login_required
def verCodigosCliente(request,id):
    clienteactual= models.Cliente.objects.get(pk=id)
    fechas = models.PerfilMascotas.objects.filter(cliente=clienteactual).datetimes('created_date', 'day')
    fecha_elegida = request.GET.get('fecha', None)
    if fecha_elegida:
        fecha_elegida = datetime.strptime(fecha_elegida, '%Y-%m-%d')
        codigos = models.PerfilMascotas.objects.filter(cliente=clienteactual, created_date__date=fecha_elegida)
    else:
        codigos = models.PerfilMascotas.objects.filter(cliente=clienteactual)
    conteo_fechas = {}
    for fecha in fechas:
        conteo_fechas[fecha.date()] = models.PerfilMascotas.objects.filter(cliente=clienteactual, created_date__date=fecha.date()).count()
    return render(request, 'adminCodigos/verCodigos.html', {'codigos': codigos, 'fechas': fechas, 'conteo_fechas': conteo_fechas, 'fecha_elegida': fecha_elegida,'idcliente':id})

@login_required
def imprimir(request):
    if request.method=="POST":
        seleccionar = request.POST.getlist('seleccionar')
        diseno= request.POST.getlist('diseno')
        if seleccionar:
            if diseno:
                codigos=models.PerfilMascotas.objects.filter(pk__in=seleccionar)
                
                for codigo in codigos:
                    url = codigo.idperfil
                    codigo_qr = pyqrcode.create(url)
                    buffer = io.BytesIO()
                    codigo_qr.png(buffer, scale=6)
                    img_bytes = buffer.getvalue()
                    img_bytes_base64 = base64.b64encode(img_bytes)
                    codigo.img_bytes_base64 = img_bytes_base64
                    
                return render(request, 'adminCodigos/codigoDiseno.html',{'codigos':codigos})
            else:
                codigos=models.PerfilMascotas.objects.filter(pk__in=seleccionar)
                
                for codigo in codigos:
                    url = codigo.idperfil
                    codigo_qr = pyqrcode.create(url)
                    buffer = io.BytesIO()
                    codigo_qr.png(buffer, scale=20)
                    img_bytes = buffer.getvalue()
                    img_bytes_base64 = base64.b64encode(img_bytes)
                    codigo.img_bytes_base64 = img_bytes_base64
                    
                return render(request, 'adminCodigos/soloCodigo.html',{'codigos':codigos})
            # hacer algo con los id seleccionados
        else:
            pass
            # mostrar mensaje de error
            
            
            

            
            
            
            
@login_required
def imprimirRecientes(request,cliente):
    # Obtiene todos los códigos QR de la tabla "codigos"
    dateNow = datetime.now()
    dateNow_min = datetime.combine(dateNow, time.min)
    dateNow_max = datetime.combine(dateNow, time.max)
    clienteactual= models.Cliente.objects.get(pk=cliente)
    codigos=models.PerfilMascotas.objects.filter(created_date__range=(dateNow_min, dateNow_max)).filter(cliente=clienteactual)
    
    for codigo in codigos:
        url = codigo.idperfil
        codigo_qr = pyqrcode.create(url)
        buffer = io.BytesIO()
        codigo_qr.png(buffer, scale=6)
        img_bytes = buffer.getvalue()
        img_bytes_base64 = base64.b64encode(img_bytes)
        codigo.img_bytes_base64 = img_bytes_base64
    
    return render(request, 'adminCodigos/codigoDiseno.html',{'codigos':codigos})

            
@login_required
def eliminarCodigo(request,idcodigo,id):
    codigo=models.PerfilMascotas.objects.get(pk=idcodigo)
    if codigo.imagenPerfil:
        # obteniendo la ruta de la imagen
        image_path = codigo.imagenPerfil.path
        codigo.delete()
        # eliminando la imagen del servidor
        os.remove(image_path)
    else:
        codigo.delete()
        
    return redirect('verCodigosCliente',id)


@login_required
def eliminarCliente(request,id):
    cliente = models.Cliente.objects.get(pk=id)
    # obteniendo la ruta de la imagen
    image_path = cliente.logo.path
    # eliminando el cliente
    cliente.delete()
    # eliminando la imagen del servidor
    os.remove(image_path)
    return redirect('clientes')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('clientes')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'adminCodigos/login.html', {'error': 'Invalid login credentials','form': form})
    else:
        form = AuthenticationForm(request.POST)
        return render(request, 'adminCodigos/login.html',{'form': form})
    

def logout_view(request):
    logout(request)
    return redirect('login')

