from django import forms
from decimal import *

class FacturaForm(forms.Form):
    nombre = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput"}))
    apellido = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput"}))
    cedula = forms.IntegerField(widget=forms.TextInput(attrs={"class": "textInput"}))
    codigo = forms.IntegerField(required=False,widget=forms.TextInput(attrs={"class": "textInput"}))
    cantidad = forms.IntegerField(required=False,widget=forms.TextInput(attrs={"class": "textInput"}))
    divisas = forms.DecimalField(required=False,max_digits=10, decimal_places=2, initial=Decimal(0.00), widget=forms.TextInput(attrs={"class": "textInput", "style":"text-align:right", "size": "18"}))