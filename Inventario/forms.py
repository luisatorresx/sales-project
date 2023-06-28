from django import forms

class ProductoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    codigo = forms.IntegerField()
    precio = forms.DecimalField(max_digits=10, decimal_places=2)
    stock = forms.IntegerField()
