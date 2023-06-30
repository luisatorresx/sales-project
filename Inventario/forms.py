from django import forms

class ProductoForm(forms.Form):
    nombre = forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class": "textInput"}))
    codigo = forms.IntegerField(widget=forms.TextInput(attrs={"class": "textInput"}))
    precio = forms.DecimalField(max_digits=10, decimal_places=2,widget=forms.TextInput(attrs={"class": "textInput"}))
    stock = forms.IntegerField(widget=forms.TextInput(attrs={"class": "textInput"}))
    proveedor = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "textInput"}))
