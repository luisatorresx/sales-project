from django.shortcuts import render, redirect
from django.http import HttpResponse
from Inventario.models import Productos
from .forms import FacturaForm

# Create your views here.
def index(request):
    return render(request, 'Ventas/index.html')

def facturacion(request):
    
    if request.method == "POST":
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = {'NumeroDeFactura': request.POST['NumeroDeFactura'], 'NombreCompleto': request.POST['NombreCompleto'], 'Cedula': request.POST['Cedula'], 'Total': request.POST['Total'], 'CodigoProducto': request.POST['CodigoProducto']}
            return render(request, 'Ventas/FacturaAImprimir.html', {'factura': factura})
    
    else:
        form = FacturaForm()
        return render(request, 'Ventas/Facturacion.html', {'form': form})


#def FacturaAImprimir(request):
  #  return  render(request, 'Ventas/FacturaAImprimir.html')