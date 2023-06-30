from django.shortcuts import render
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
            form.full_clean()
            return render(request, 'Ventas/Facturacion.html', {'form': form})
    
    else:
        form = FacturaForm()
        return render(request, 'Ventas/Facturacion.html', {'form': form})
