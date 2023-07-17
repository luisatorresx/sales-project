from django.shortcuts import render
from django.db import models
from Inventario.models import Productos
from .forms import FacturaForm
from decimal import *

# Create your views here.
def index(request):
    return render(request, 'Ventas/index.html')



def facturacion(request):
    
    subtotal = Decimal(0.00)
    iva = Decimal(0.00)
    subtotaliva = Decimal(0.00)
    IGTF = Decimal(0.00)
    total = Decimal(0.00)
    totaldolares = Decimal(0.00)
    fraccionBS = Decimal(0.00)

    if request.method == "POST":
        print("""inicio
              ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
              ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
              """)
        #print(request.POST)
        form = FacturaForm(request.POST)
        procutosFactura = []
        productos = Productos.objects.all()
        for producto in productos:
            if str(producto.codigo) in request.POST:
                #print(producto.codigo)
                procutosFactura.append([Productos.objects.filter(codigo=producto.codigo), int(request.POST[str(producto.codigo)])])
        #print(procutosFactura)

        if form.is_valid():
            if "añadir" in request.POST:
                if request.POST['codigo'] != '' and request.POST['cantidad'] != '':
                    if productos.filter(codigo=request.POST['codigo']).exists():
                        procutosFactura.append([productos.filter(codigo=request.POST['codigo']), int(request.POST['cantidad'])])
                #print(procutosFactura)

            if "eliminar" in request.POST:
                for producto in procutosFactura:
                    if str(producto[0][0].codigo) == request.POST['eliminar']:
                        procutosFactura.pop(procutosFactura.index(producto))

            
            clearFields = request.POST.copy()
            if "codigo" in clearFields:
                clearFields["codigo"] = ''
            if "cantidad" in clearFields:
                clearFields["cantidad"] = ''
            form = FacturaForm(clearFields)

            print(procutosFactura)
            for producto in procutosFactura:
                print(producto[0], producto[1])
            
        
        return render(request, 'Ventas/Facturacion.html', {'form': form, 'procutosFactura': procutosFactura, 'subtotal': subtotal, 
                                                            'total': total, 'iva': iva, 'IGTF': IGTF, 'subtotaliva': subtotaliva, 
                                                            'totaldolares': totaldolares, 'fraccionBS': fraccionBS})
    else:
        procutosFactura = []
        form = FacturaForm()
        return render(request, 'Ventas/Facturacion.html', {'form': form, 'procutosFactura': procutosFactura, 'subtotal': subtotal, 
                                                           'total': total, 'iva': iva, 'IGTF': IGTF, 'subtotaliva': subtotaliva, 
                                                           'totaldolares': totaldolares, 'fraccionBS': fraccionBS})
