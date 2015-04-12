from django import forms
from django.forms import ModelForm
from models import *

class CategoriaForm(forms.Form):
	nombre = forms.CharField(widget=forms.TextInput(attrs={ 'required': 'true','placeholder':'Nombre de la categoría' }),label='')
    descripcion=forms.TextInput(widget=forms.TextInput(attrs={ 'required': 'true','placeholder':'Nombre de la categoría',
    'class':'editor' }),label='')


