from django import forms

class ProductoForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Nombre del producto"}))

    codigo = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "textInput", "placeholder": "Código del producto"}))

    precio = forms.DecimalField(decimal_places=2, widget=forms.NumberInput(attrs={"class": "textInput", "placeholder": "Precio del producto"}))

    stock = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "textInput", "placeholder": "Stock disponible"}))

    proveedor = forms.CharField(widget=forms.TextInput(attrs={"class": "textInput", "placeholder": "Nombre del proveedor"}))
