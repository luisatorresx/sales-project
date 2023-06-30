from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(label=('Nombre de usuario'), max_length=50, widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Introduzca nombre de usuario"}))
    email = forms.EmailField(label=('Correo electrónico'), widget=forms.EmailInput(attrs={"class": "textInput", "placeholder": "Introduzca correo electrónico"}))
    password = forms.CharField(label=('Contraseña'), widget=forms.PasswordInput(attrs={"class": "textInput", "placeholder": "Introduzca contraseña"}))
    first_name = forms.CharField(label=('Nombre'), max_length=30, required=False, widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Introduzca nombre"}))
    last_name = forms.CharField(label=('Apellido'), max_length=150, required=False, widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Introduzca apellido"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
