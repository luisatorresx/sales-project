from django.shortcuts import render
from django.db import models
from Inventario.models import Productos
from .forms import FacturaForm
from decimal import *

# Create your views here.
def index(request):
    return render(request, 'Ventas/index.html')



def facturacion(request):
    
    # Asignando valores por defecto
    subtotal = Decimal(0.00)
    iva = Decimal(0.00)
    subtotaliva = Decimal(0.00)
    IGTF = Decimal(0.00)
    total = Decimal(0.00)
    totaldolares = Decimal(0.00)
    fraccionBS = Decimal(0.00)
    
    # Errores
    Producto_no_entocntrado = False
    Campo_en_blanco = False
    Producto_insuficiente = False


    if request.method == "POST":
        print("""inicio
              ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
              ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
              """)
        # Copiando información para la siguiente respuesta
        form = FacturaForm(request.POST)
        procutosFactura = []
        productos = Productos.objects.all()
        for producto in productos:
            if str(producto.codigo) in request.POST:
                procutosFactura.append([Productos.objects.filter(codigo=producto.codigo), int(request.POST[str(producto.codigo)])])

        if form.is_valid():

            # Añadir producto
            if "añadir" in request.POST:
                if request.POST['codigo'] != '' and request.POST['cantidad'] != '': # Verifica si los campos del producto a añadir fueron llenados
                    if productos.filter(codigo=request.POST['codigo']).exists():    # Verifica si el prodcuto existe
                        if productos.filter(codigo=request.POST['codigo'])[0].stock >= int(request.POST['cantidad']):
                            for producto in procutosFactura:                            # Elimina el producto duplicado de la lista para permitir la sobrescritura
                                if str(producto[0][0].codigo)==request.POST['codigo']: 
                                    procutosFactura.pop(procutosFactura.index(producto))
                            procutosFactura.append([productos.filter(codigo=request.POST['codigo']), int(request.POST['cantidad'])]) # Añade el producto y lña cantidad del mismo a la lista
                        else:
                            Producto_insuficiente = [True, productos.filter(codigo=request.POST['codigo'])[0].stock]
                    else:
                        Producto_no_entocntrado = True
                else:
                    Campo_en_blanco = True

            # Eliminar producto
            if "eliminar" in request.POST:
                for producto in procutosFactura:
                    if str(producto[0][0].codigo) == request.POST['eliminar']:
                        procutosFactura.pop(procutosFactura.index(producto))

            # Limpiar entrada productos
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
                                                            'totaldolares': totaldolares, 'fraccionBS': fraccionBS, 
                                                            'Producto_no_entocntrado':Producto_no_entocntrado, 'Campo_en_blanco':Campo_en_blanco, 'Producto_insuficiente':Producto_insuficiente})
    else:
        procutosFactura = []
        form = FacturaForm()
        return render(request, 'Ventas/Facturacion.html', {'form': form, 'procutosFactura': procutosFactura, 'subtotal': subtotal, 
                                                           'total': total, 'iva': iva, 'IGTF': IGTF, 'subtotaliva': subtotaliva, 
                                                           'totaldolares': totaldolares, 'fraccionBS': fraccionBS})
