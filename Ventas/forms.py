from django import forms
from decimal import *

class FacturaForm(forms.Form):
    nombre = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput", "onkeydown":"return /[a-záéíóúñü]/i.test(event.key)", "autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    apellido = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput", "onkeydown":"return /[a-záéíóúñü]/i.test(event.key)", "autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    cedula = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "textInput", "min":"1", "step":"1","onkeydown":"if(event.key==='.'){event.preventDefault();}","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    codigo = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class": "textInput", "min":"0", "step":"1","onkeydown":"if(event.key==='.'){event.preventDefault();}","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    cantidad = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class": "textInput", "min":"1", "step":"1","onkeydown":"if(event.key==='.'){event.preventDefault();}","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    divisas = forms.DecimalField(required=False,max_digits=10, decimal_places=2, initial=Decimal(0.00), widget=forms.NumberInput(attrs={"class": "textInput", "style":"text-align:right", "size": "18", "autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
