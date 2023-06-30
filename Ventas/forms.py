from django import forms

class FacturaForm(forms.Form):
    NumeroDeFactura = forms.IntegerField(widget=forms.TextInput(attrs={"class": "textInput"}))
    NombreCompleto = forms.CharField(max_length=50,widget=forms.TextInput(attrs={"class": "textInput"}))
    Cedula = forms.IntegerField(widget=forms.TextInput(attrs={"class": "textInput"}))
    Total = forms.DecimalField(max_digits=10, decimal_places=2,widget=forms.TextInput(attrs={"class": "textInput"}))
    CodigoProducto = forms.IntegerField(widget=forms.TextInput(attrs={"class": "textInput"}))
