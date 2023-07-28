from decimal import Decimal
from django import forms
from django.contrib.auth.models import User

Roles = (
    ("Empleado", "Empleado"),
    ("Almacenista", "Almacenista"),
    ("Analista de datos", "Analista de datos"),
    ("Administrador", "Administrador"),
    )

class UserForm(forms.ModelForm):
    username = forms.CharField(label=('Nombre de usuario'), max_length=50, widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Nombre de usuario"}))
    email = forms.EmailField(label=('Correo electrónico'), widget=forms.EmailInput(attrs={"class": "textInput", "placeholder": "Correo electrónico"}))
    password = forms.CharField(label=('Contraseña'), widget=forms.PasswordInput(attrs={"class": "textInput", "placeholder": "Contraseña"}))
    first_name = forms.CharField(label=('Nombre'), max_length=30, required=False, widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Nombres"}))
    last_name = forms.CharField(label=('Apellido'), max_length=150, required=False, widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Apellidos"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class GroupForm(forms.Form):
    rol = forms.ChoiceField(choices = Roles)
        
class LoginForm(forms.Form):
    username = forms.CharField(label=('Nombre de usuario'), max_length=50, widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Nombre de usuario"}))
    password = forms.CharField(label=('Contraseña'), widget=forms.PasswordInput(attrs={"class": "textInput", "placeholder": "Contraseña"}))

class TipoDeCambioForm(forms.Form):
    cambio = forms.DecimalField(required=False,max_digits=10, decimal_places=4, initial=Decimal(0.0000).quantize(Decimal('.0001')), widget=forms.NumberInput(attrs={"class": "textInput", "style":"text-align:right; width:100px; margin-right:0px;", "size": "18", "min":"0", "step":"0.0001","autocomplete":"off", "onCopy":"return false", "onDrag":"return false", "onDrop":"return false", "onPaste":"return false", "onkeydown":"if(event.keyCode == 13){event.preventDefault();}","onchange":"this.value = parseFloat(this.value).toFixed(4);"}))
