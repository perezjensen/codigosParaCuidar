from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Cliente
from web.models import Pais
from perfilMascotas.models import PerfilMascotas
import re


    



class ClienteForm(forms.ModelForm):
    
    nombreCliente = forms.CharField(required=False)
    nombreNegocio = forms.CharField(required=True, error_messages={'required': 'El nombre del negocio es obligatorio'})
    telefono = forms.CharField(required=False)
    correo = forms.EmailField(required=False)
    direccion = forms.CharField(required=False)
    ciudad = forms.CharField(required=False)
    logo=forms.ImageField(required=True, error_messages={'required': 'Debes agregar un logo'})
    observaciones=forms.CharField(required=False)
    tictok=forms.CharField(required=False)
    facebook=forms.CharField(required=False)
    instagram=forms.CharField(required=False)
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), error_messages={'required': 'Debes agregar un cliente'})
    
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if not "@" in correo:
            raise ValidationError("El correo debe tener una @")
        if not "." in correo:
            raise ValidationError("El correo debe tener un punto")
        return correo
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']

        if telefono is not None:
            telefono = telefono.strip()
        else:
            telefono = ""
        
            # Verifica si el número de teléfono tiene solo dígitos
        if not telefono.isdigit():
            raise forms.ValidationError('El número de teléfono debe contener solo dígitos')

        # Deja solo números en el número de teléfono
        telefono = re.sub(r'\D', '', telefono)


        return telefono
    class Meta:
        model=Cliente
        fields = ['nombreNegocio','nombreCliente','telefono','correo','direccion','ciudad','logo','observaciones','tictok','facebook','instagram','pais']
        
        
class EditarClienteForm(forms.ModelForm):
    
    nombreCliente = forms.CharField(required=False)
    nombreNegocio = forms.CharField(required=True, error_messages={'required': 'El nombre del negocio es obligatorio'})
    telefono = forms.CharField(required=False)
    correo = forms.EmailField(required=False)
    direccion = forms.CharField(required=False)
    ciudad = forms.CharField(required=False)
    observaciones=forms.CharField(required=False)
    tictok=forms.CharField(required=False)
    facebook=forms.CharField(required=False)
    instagram=forms.CharField(required=False)
    
    
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if not "@" in correo:
            raise ValidationError("El correo debe tener una @")
        if not "." in correo:
            raise ValidationError("El correo debe tener un punto")
        return correo
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']

        if telefono is not None:
            telefono = telefono.strip()
        else:
            telefono = ""
        
            # Verifica si el número de teléfono tiene solo dígitos
        if not telefono.isdigit():
            raise forms.ValidationError('El número de teléfono debe contener solo dígitos')

        # Deja solo números en el número de teléfono
        telefono = re.sub(r'\D', '', telefono)


        return telefono
    class Meta:
        model=Cliente
        fields = ['nombreNegocio','nombreCliente','telefono','correo','direccion','ciudad','observaciones','tictok','facebook','instagram',]
    

        
        
class GenerarCodigo(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), error_messages={'required': 'Debes agregar un cliente'})
    precio = forms.FloatField(required=False)

    class Meta:
        model=PerfilMascotas
        fields = ['cliente','precio']
        
