from django import forms
from decimal import *

class ProductoForm(forms.Form):
    nombre = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput", "onkeydown":"return /[a-záéíóúñü]/i.test(event.key)", "autocomplete":"on", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "placeholder":"Nombre"}))

    codigo = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "textInput", "min":"1", "step":"1","onkeydown":"if(event.key==='.'){event.preventDefault();}","autocomplete":"on", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "placeholder":"Código"}))

    precio = forms.DecimalField(required=False,max_digits=10, decimal_places=2, initial=Decimal(0.00).quantize(Decimal('.01')), widget=forms.NumberInput(attrs={"class": "textInput", "autocomplete":"on", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "onchange":"this.value = parseFloat(this.value).toFixed(2);", "placeholder":"Precio"}))

    stock = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "textInput", "min":"1", "step":"1","onkeydown":"if(event.key==='.'){event.preventDefault();}","autocomplete":"on", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "placeholder":"Unidades"}))

    proveedor = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput", "onkeydown":"return /[a-záéíóúñü]/i.test(event.key)", "autocomplete":"on", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "placeholder":"Proveedor"}))

    iva = forms.IntegerField(widget=forms.NumberInput(attrs={"'value': '16', class": "textInput", "min":"1", "step":"1","onkeydown":"if(event.key==='.'){event.preventDefault();}","autocomplete":"on", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "placeholder": "IVA"}))
