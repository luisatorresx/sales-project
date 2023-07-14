from django import forms

class ProductoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    codigo = forms.IntegerField()
    precio = forms.DecimalField(decimal_places=2)
    stock = forms.IntegerField()
    proveedor = forms.CharField()
