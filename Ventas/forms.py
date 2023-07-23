from django import forms
from decimal import *


Persona =(
    ("0", "V-"),
    ("1", "E-"),
    ("2", "J-"),
)

class FacturaForm(forms.Form):
    nombre = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput", "onkeydown":"if(event.key==='.'||event.keyCode == 13){event.preventDefault();}return /[a-záéíóúñü]/i.test(event.key)", "autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    apellido = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput", "onkeydown":"if(event.key==='.'||event.keyCode == 13){event.preventDefault();}return /[a-záéíóúñü]/i.test(event.key)", "autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    cedula = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "textInput", "min":"1", "step":"1","style":"width:140px;","onkeydown":"if(event.key==='.'||event.keyCode == 13){event.preventDefault();}","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    codigo = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class": "textInput", "min":"0", "step":"1","onkeydown":"if(event.key==='.'||event.keyCode == 13){event.preventDefault();}","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    cantidad = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class": "textInput", "min":"1", "step":"1","onkeydown":"if(event.key==='.'||event.keyCode == 13){event.preventDefault();}","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false"}))
    divisas = forms.DecimalField(required=False,max_digits=10, decimal_places=2, initial=Decimal(0.00).quantize(Decimal('.01')), widget=forms.NumberInput(attrs={"class": "textInput", "style":"text-align:right; width:100px; margin-right:0px;", "size": "18", "min":"0", "step":"0.01","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "onkeydown":"if(event.keyCode == 13){event.preventDefault();}","onchange":"this.value = parseFloat(this.value).toFixed(2);"}))
    efectivo = forms.DecimalField(required=False,max_digits=10, decimal_places=2, initial=Decimal(0.00).quantize(Decimal('.01')), widget=forms.NumberInput(attrs={"class": "textInput", "style":"text-align:right; width:100px; margin-right:0px;", "size": "18", "min":"0", "step":"0.01","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "onkeydown":"if(event.keyCode == 13){event.preventDefault();}","onchange":"this.value = parseFloat(this.value).toFixed(2);"}))
    tipo = forms.ChoiceField(choices=Persona)