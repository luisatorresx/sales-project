from django.shortcuts import render, redirect, get_object_or_404
from Inventario.models import Productos
from django.core.paginator import Paginator
from .forms import FacturaForm
from decimal import *
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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

            if "concretar" in request.POST:

                if pago_completo:

                    tipo_de_cambio = models.HistorialTipoDeCambio.objects.get_or_create(
                        cambio = dolar_Bs_cambio
                    )

                    cliente = models.Clientes.objects.get_or_create(
                        cedula = request.POST['cedula'],
                        nombre = request.POST['nombre'],
                        apellido = request.POST['apellido'],
                        tipo = int(request.POST['tipo'])
                    )
                    
                    factura = models.Facturas.objects.create(
                        total_base = subtotal,
                        iva = iva,
                        cancelado_en_divisa = Cantidad_divisa,
                        impuesto_divisa = Igft_res, #en bs
                        cancelado_en_bs = Cantidad_Bs,
                        total = subtotal_iva + Igft_res,
                        id_cliente = cliente[0],
                        id_tipo_de_cambio = tipo_de_cambio[0],
                        vuelto = Vuelto
                    )

                    for producto in procutosFactura:

                        identificador_producto = models.IdentificadorProductos.objects.get_or_create(
                            nombre = producto[0][0].nombre,
                            codigo = producto[0][0].codigo
                        )
                        
                        producto_añadido = models.HistorialProductos.objects.get_or_create(
                            iva = producto[0][0].iva,
                            precio = producto[0][0].precio,
                            cantidad = producto[1],
                            producto = identificador_producto[0]
                        )
                                                
                        producto_almacen = get_object_or_404(Productos, id=producto[0][0].id)
                        producto_almacen.stock -= producto[1]
                        producto_almacen.save()

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
        productos_base = factura.productos.all()
        productos = []
        base_imponible_G = Decimal(0.00)
        base_imponible_R = Decimal(0.00)
        iva_G = Decimal(0.00)
        iva_R = Decimal(0.00)
        exento = Decimal(0.00)
        pagado_en_dolares = Decimal(0.00)
        documento = ''
        
        if factura.id_cliente.tipo == 0:
            persona = "V-" 
        elif factura.id_cliente.tipo == 1:
            persona = "V-"
            documento = f'{factura.id_cliente.cedula:09d}'
        elif factura.id_cliente.tipo == 2:
            persona = "E-"
        elif factura.id_cliente.tipo == 3:
            persona = "E-"
            documento = f'{factura.id_cliente.cedula:09d}'
        else:
            persona = "J-"
            documento = f'{factura.id_cliente.cedula:09d}'
            print(documento)

        for producto in productos_base:
            if producto.iva == 0:
                iva = "(E)"
                exento += producto.precio * producto.cantidad 
            else:
                if producto.iva == 1:
                    iva = "(G)"
                    iva_G += (producto.precio * producto.cantidad * Decimal(0.16)).quantize(Decimal('.01'))
                    base_imponible_G += producto.precio * producto.cantidad 
                else:
                    iva = "(R)" 
                    iva_R += (producto.precio * producto.cantidad * Decimal(0.08)).quantize(Decimal('.01'))
                    base_imponible_R += producto.precio * producto.cantidad 
            productos.append([producto, (producto.cantidad * producto.precio).quantize(Decimal('.01')), iva])

        en_divisas = (factura.cancelado_en_divisa * factura.id_tipo_de_cambio.cambio).quantize(Decimal('.01'))
        if en_divisas > (factura.total_base + factura.iva):
            pagado_en_dolares = factura.total_base + factura.iva
        else:
            pagado_en_dolares = en_divisas

        fecha = factura.fecha.strftime('%d-%m-%Y')
        hora = factura.fecha.strftime('%H:%M:%S')

        return render(request, 'Ventas/Factura.html', {'id':f'{id:09d}', 'factura':factura, 'productos':productos, 'fecha':fecha, 'hora':hora,
                                                    'base_imponible_G':base_imponible_G, 'base_imponible_R':base_imponible_R, 'iva_G':iva_G, 'iva_R':iva_R, 
                                                    'exento':exento, 'en_divisas':en_divisas, 'pagado_en_dolares':pagado_en_dolares, 'persona':persona, 'documento':documento})
    except:
        return redirect('error_ventas', id=id)
    
def error(request,id):
    return render(request, 'Ventas/Error.html', {'id':f'{id:09d}'})

def historial_facturas(request):

    facturas = models.Facturas.objects.all()
    lista_facturas = []

    for factura in facturas:
        f_num = f'{factura.id:09d}'
        if factura.id_cliente.tipo == 4:
            persona = "J-"
            lista_facturas.append([factura, f'{persona}{factura.id_cliente.cedula:09d}', f_num])
        elif factura.id_cliente.tipo == 3:
            persona = "E-"
            lista_facturas.append([factura, f'{persona}{factura.id_cliente.cedula:09d}', f_num])
        elif factura.id_cliente.tipo == 2:
            persona = "E-"
            lista_facturas.append([factura, f'{persona}{factura.id_cliente.cedula}', f_num])
        elif factura.id_cliente.tipo == 1:
            persona = "V-"
            lista_facturas.append([factura, f'{persona}{factura.id_cliente.cedula:09d}', f_num])
        else:
            persona = "V-"
            lista_facturas.append([factura, f'{persona}{factura.id_cliente.cedula}', f_num])
    
    page_number = request.GET.get('page')

    if request.method == "POST":
        print(request.POST['salto'])
        if request.POST['salto'] != '' and int(request.POST['salto']) >= 1:
            page_number = request.POST['salto']
        else:
            page_number = request.POST['page']

    lista_facturas.reverse()
    paginator = Paginator(lista_facturas, 50)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Ventas/Registro_Facturas.html', {'page_obj': page_obj})
