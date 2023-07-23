from django.shortcuts import render, redirect, get_object_or_404
from Inventario.models import Productos
from .forms import FacturaForm
from decimal import *
from . import models

# Create your views here.
def index(request):
    return render(request, 'Ventas/index.html')

def facturacion(request):
    
    # Asignando valores por defecto
    decimales = '.01'
    dolar_Bs_cambio = Decimal(28.8123)
    subtotal = Decimal(0.00).quantize(Decimal(decimales))
    iva = Decimal(0.00).quantize(Decimal(decimales))
    subtotal_iva = Decimal(0.00).quantize(Decimal(decimales))
    en_dolares = Decimal(0.00).quantize(Decimal(decimales))
    Igft = Decimal(0.00).quantize(Decimal(decimales))
    total_dolares = Decimal(0.00).quantize(Decimal(decimales))
    total = Decimal(0.00).quantize(Decimal(decimales))
    fraccionBS = Decimal(0.00).quantize(Decimal(decimales))
    Igft_res_US = Decimal(0.00).quantize(Decimal(decimales))
    Igft_res = Decimal(0.00).quantize(Decimal(decimales))
    Vuelto = Decimal(0.00).quantize(Decimal(decimales))
    Cantidad_divisa = Decimal(0.00).quantize(Decimal(decimales))
    Cantidad_Bs = Decimal(0.00).quantize(Decimal(decimales))

    # Errores
    Producto_no_entocntrado = False
    Campo_en_blanco = False
    Producto_insuficiente = False
    pago_completo = True
    pago_incompleto = False

    if request.method == "POST":
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
                if request.POST['codigo'] != '' and request.POST['cantidad'] != '':                                     # Verifica si los campos del producto a añadir fueron llenados
                    if productos.filter(codigo=request.POST['codigo']).exists():                                        # Verifica si el prodcuto existe
                        if productos.filter(codigo=request.POST['codigo'])[0].stock >= int(request.POST['cantidad']):   # Verifica que existan suficientes unidades en stock para la solicitud
                            for producto in procutosFactura:                                                            # Elimina el producto duplicado de la lista para permitir la sobrescritura
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

            # Calcular precio
            #if not ("concretar" in request.POST):

            # Subtotal
            for producto in procutosFactura:
                subtotal += producto[0][0].precio * producto[1]
                if producto[0][0].iva == 1:
                    iva += (producto[0][0].precio * producto[1] * Decimal(0.16)).quantize(Decimal(decimales))
                else:
                    if producto[0][0].iva == 2:
                        iva += (producto[0][0].precio * producto[1] * Decimal(0.08)).quantize(Decimal(decimales))
            subtotal_iva = subtotal + iva
            en_dolares = (subtotal_iva / dolar_Bs_cambio).quantize(Decimal(decimales))
            Igft = (en_dolares * Decimal(0.03)).quantize(Decimal(decimales))
            total_dolares = en_dolares + Igft
            if request.POST['divisas'] != '':
                if Decimal(request.POST['divisas']) >= 0:
                    Cantidad_divisa = Decimal(request.POST['divisas'])
                    if Cantidad_divisa <= en_dolares:
                        Divsas_en_Bs = (Cantidad_divisa * dolar_Bs_cambio).quantize(Decimal(decimales))
                        Igft_res_US = (Cantidad_divisa * Decimal(0.03)).quantize(Decimal(decimales))
                        Igft_res = (Divsas_en_Bs * Decimal(0.03)).quantize(Decimal(decimales))
                        fraccionBS = subtotal_iva - Divsas_en_Bs + Igft_res
                    else:
                        Igft_res_US = Igft
                        Igft_res = (subtotal_iva * Decimal(0.03)).quantize(Decimal(decimales))
                        Divsas_en_Bs = (Cantidad_divisa * dolar_Bs_cambio).quantize(Decimal(decimales))
                        fraccionBS = subtotal_iva - Divsas_en_Bs + Igft_res
            if request.POST['efectivo'] != '':
                if Decimal(request.POST['efectivo']) >= 0:
                    Cantidad_Bs = Decimal(request.POST['efectivo'])
                    Vuelto = Cantidad_Bs - fraccionBS
            if fraccionBS < 0:
                fraccionBS = Decimal(0.00)

            if Vuelto < 0:
                pago_completo = False
                Vuelto = -Vuelto
            #else:

            if "concretar" in request.POST:
                if pago_completo:
                    tipo_de_cambio = models.HistorialTipoDeCambio.objects.get_or_create(
                        cambio = dolar_Bs_cambio.quantize(Decimal('.01'))
                    )

                    cliente = models.Clientes.objects.get_or_create(
                        cedula = request.POST['cedula'],
                        nombre = request.POST['nombre'],
                        apellido = request.POST['apellido']
                    )
                    
                    factura = models.Facturas.objects.create(
                        total_base = subtotal,
                        iva = iva,
                        cancelado_en_divisa = Cantidad_divisa,
                        impuesto_divisa = Igft_res, #en bs
                        cancelado_en_bs = Cantidad_Bs,
                        total = subtotal + iva + Divsas_en_Bs,
                        id_cliente = cliente[0],
                        id_tipo_de_cambio = tipo_de_cambio[0]
                    )

                    for producto in procutosFactura:

                        identificador_producto = models.IdentificadorProductos.objects.get_or_create(
                            nombre = producto[0][0].nombre,
                            codigo = producto[0][0].codigo
                        )
                        
                        producto_añadido = models.HistorialProductos.objects.get_or_create(
                            iva = producto[0][0].iva,
                            precio = producto[0][0].precio,
                            producto = identificador_producto[0]
                        )

                        factura.productos.add(producto_añadido[0])

                    return redirect('factura', id=factura.id)
                else:
                    pago_incompleto = True



            # Limpiar entrada productos
            clearFields = request.POST.copy()
            if "codigo" in clearFields:
                clearFields["codigo"] = ''
            if "cantidad" in clearFields:
                clearFields["cantidad"] = ''
            form = FacturaForm(clearFields)

            #print(procutosFactura)
            #for producto in procutosFactura:
                #print(producto[0], producto[1])
            
        
        return render(request, 'Ventas/Facturacion.html', {'form': form, 'procutosFactura': procutosFactura, 'subtotal': subtotal, 
                                                            'total': total, 'iva': iva, 'Igft': Igft, 'subtotal_iva': subtotal_iva, "Igft_res_US":Igft_res_US, "Igft_res":Igft_res,
                                                            'en_dolares':en_dolares,'total_dolares': total_dolares, 'fraccionBS': fraccionBS, 'Vuelto':Vuelto, 'pago_completo':pago_completo,
                                                            'Producto_no_entocntrado':Producto_no_entocntrado, 'Campo_en_blanco':Campo_en_blanco, 'Producto_insuficiente':Producto_insuficiente,
                                                            'pago_incompleto':pago_incompleto})
    else:
        procutosFactura = []
        form = FacturaForm()
        return render(request, 'Ventas/Facturacion.html', {'form': form, 'procutosFactura': procutosFactura, 'subtotal': subtotal, 
                                                            'total': total, 'iva': iva, 'Igft': Igft, 'subtotal_iva': subtotal_iva, "Igft_res_US":Igft_res_US, "Igft_res":Igft_res,
                                                            'en_dolares':en_dolares,'total_dolares': total_dolares, 'fraccionBS': fraccionBS, 'Vuelto':Vuelto, 'pago_completo':pago_completo,
                                                            'Producto_no_entocntrado':Producto_no_entocntrado, 'Campo_en_blanco':Campo_en_blanco, 'Producto_insuficiente':Producto_insuficiente,
                                                            'pago_incompleto':pago_incompleto})
    
def factura(request, id):

    try:
        factura = get_object_or_404(models.Facturas, id = id)
        productos = factura.productos.all()
        return render(request, 'Ventas/Factura.html', {'id':f'{id : 07d}', 'factura':factura, 'productos':productos})
    except:
        return redirect('error_ventas', id=id)
    
def error(request,id):
    return render(request, 'Ventas/Error.html', {'id':f'{id : 07d}'})

def historial_facturas(request):
    return render(request, 'Ventas/Error.html')
