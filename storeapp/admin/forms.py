from django import forms
from django.forms import ModelForm
from models import *

class UsuarioForm(ModelForm):
	
    class Meta:
        model  = Usuario
        fields = '__all__'
        labels = {
            'Negocio': (''),
            'Nombre':(''),
            'Email':('')
        }

        nombre = forms.CharField(widget=forms.TextInput(attrs={ 'required': 'true','placeholder':'Tu nombre completo' }),label='')
        correo = forms.EmailField(widget=forms.TextInput(attrs={ 'required': 'true','placeholder':'ejemplo@correo.com','labels':'','type':'email', }),label='')
        negocio = forms.CharField(widget=forms.TextInput(attrs={ 'required': 'true','placeholder':'negocio','labels':'' }),label='')

