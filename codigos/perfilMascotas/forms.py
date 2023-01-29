from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import PerfilMascotas, vacuna, bano, desparasitante, peso
from web.models import Pais
import re



        

class UpdateImage(forms.ModelForm):
    
    imagenPerfil=forms.ImageField(required=True, error_messages={'required': 'Debes agregar una foto'})

    class Meta:
        model=PerfilMascotas
        fields = ['imagenPerfil']


class CreatePerfil(forms.ModelForm):
    nombreMascota = forms.CharField(required=True, error_messages={'required': 'Este campo es obligatorio'})
    correo = forms.EmailField(required=True,error_messages={'required': 'Este campo es obligatorio'})
    nombreDueno = forms.CharField(required=True,error_messages={'required': 'Este campo es obligatorio'})
    imagenPerfil=forms.ImageField( required=True,error_messages={'required': 'Para completar tu perfil de mascota, es necesario subir una foto. Haz clic en el botón  "Subir Foto"  para seleccionar una imagen de tu dispositivo.'})
    telefono = forms.CharField(required=True,error_messages={'required': 'Este campo es obligatorio'})
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), error_messages={'required': 'Debes agregar un cliente'})
    
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if not "@" in correo:
            raise ValidationError("El correo debe tener una @")
        if not "." in correo:
            raise ValidationError("El correo debe tener un punto")
        return correo
    

 


    
    class Meta:
        model=PerfilMascotas
        fields = ['nombreMascota','telefono','correo','nombreDueno','imagenPerfil','pais']

class CreateVacunas(forms.ModelForm):
    fecha = forms.CharField(required=True, error_messages={'required': 'Debe agregar una fecha en el campo fecha antes de guardar.'})
    vacuna = forms.CharField(required=True,error_messages={'required': 'Debe agregar un nombre de la vacuna antes de guardar.'})
    dosis = forms.CharField(required=True,error_messages={'required': 'Debe agregar una dosis en el campo dosis antes de guardar.'})
   
    class Meta:
        model=vacuna
        fields = ['fecha','vacuna','dosis']
        
class CreateBano(forms.ModelForm):
    fecha = forms.CharField(required=True, error_messages={'required': 'Debe agregar una fecha en el campo fecha antes de guardar.'})
    descripcion = forms.CharField(required=True,error_messages={'required': 'Debe agregar una descripcion sobre el servicio.'})
   
    class Meta:
        model=bano
        fields = ['fecha','descripcion']
        
class CreateDesparasitante(forms.ModelForm):
    fecha = forms.CharField(required=True, error_messages={'required': 'Debe agregar una fecha en el campo fecha antes de guardar.'})
    antiparasitario = forms.CharField(required=True,error_messages={'required': 'Debe agregar un nombre del antiparasitario'})
    dosis = forms.CharField(required=True,error_messages={'required': 'Debe agregar una dosis '})
    
    class Meta:
        model=desparasitante
        fields = ['fecha','antiparasitario','dosis']

class CreatePeso(forms.ModelForm):
    fecha = forms.CharField(required=True, error_messages={'required': 'Debe agregar una fecha en el campo fecha antes de guardar.'})
    peso = forms.CharField(required=True,error_messages={'required': 'Debe agregar un valor para peso en el campo peso antes de guardar .'})
   
    class Meta:
        model=peso
        fields = ['fecha','peso']
        

class UdpdatePerfil(forms.ModelForm):
    
    nombreMascota = forms.CharField(required=False)
    raza = forms.CharField(required=False)
    edad = forms.CharField(required=False)
    sexo = forms.CharField(required=False)
    telefono = forms.CharField(required=False)
    correo = forms.EmailField(required=False)
    recompensa = forms.CharField(required=False)
    esterilizacion = forms.CharField(required=False)
    observaciones = forms.CharField(required=False)
    
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if not "@" in correo:
            raise ValidationError("El correo debe tener una @")
        if not "." in correo:
            raise ValidationError("El correo debe tener un punto")
        return correo
    

    class Meta:
        model=PerfilMascotas
        fields = ['nombreMascota','raza','edad','sexo','telefono','correo','recompensa','esterilizacion','observaciones']