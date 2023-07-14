from django import forms

class FacturaForm(forms.Form):
    nombre = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput"}))
    apellido = forms.CharField(max_length=30,widget=forms.TextInput(attrs={"class": "textInput"}))
    cedula = forms.IntegerField(widget=forms.TextInput(attrs={"class": "textInput"}))
