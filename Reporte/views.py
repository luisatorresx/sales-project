import random
import datetime
from django.shortcuts import render
from django.db.models import Sum, Subquery, OuterRef, F, FloatField, DecimalField, Count, Avg
from django.db.models.functions import ExtractMonth, Cast, ExtractYear
from Inventario.models import Productos, Orden_Productos, Orden_Compra
from Ventas.models import Clientes
from decimal import Decimal, ROUND_DOWN
from Ventas.models import HistorialTipoDeCambio, Clientes, IdentificadorProductos, HistorialProductos, Facturas
from faker import Faker

# Create your views here.
def data_de_productos():
    Productos.objects.all().delete()
    Orden_Compra.objects.all().delete()
    Orden_Productos.objects.all().delete()
    
    productos_por_proveedor = {
        'FrutasFrescas': [('Manzana', 0.5), ('Banana', 0.3), ('Naranja', 0.6), ('Mango', 1), ('Melocotón', 1.2)],
        'Polar': [('Harina de Maiz', 1), ('Harina de Trigo', 1.1), ('Yogurt', 2), ('Granola', 3), ('Leche de Almendra', 3), ('Tofu', 2.5), ('Barra de Proteína', 1.5)],
        'Carnicería': [('Pechuga de Pollo', 5), ('Filete de Res', 7), ('Salchichas', 4), ('Pavo', 6), ('Chuleta de Cerdo', 5.5)],
        'TierraDeDulces': [('Chocolatina', 1), ('Gomitas', 0.5), ('Paleta', 0.25), ('Pastillas', 0.75), ('Chicle', 0.1)],
        'MercaditoElGocho': [('Espinaca', 2), ('Brocoli', 2.5), ('Zanahoria', 1.5), ('Lechuga', 1.5), ('Pepino', 1)],
        'MundoVinos': [('Merlot', 15), ('Chardonnay', 12), ('Pinot Noir', 20), ('Sauvignon Blanc', 18), ('Rosado', 15)],
        'Iberia': [('Sopa de Tomate', 3), ('Maíz Dulce', 2.5), ('Frijoles Negros', 2), ('Guisantes', 2), ('Atún', 2.5)],
        'SantaTeresa': [('Whisky', 25), ('Vodka', 20), ('Ron', 15), ('Ginebra', 20), ('Tequila', 25)]
    }

    codigo = 1
    for proveedor, productos in productos_por_proveedor.items():
        for nombre_producto, precio in productos:
            Productos.objects.create(
                nombre=f'{nombre_producto} de {proveedor}',
                codigo=codigo,
                precio=precio + round(random.uniform(-1, 1), 2) if precio > 2 else precio,  # Generando precios ligeramente aleatorios alrededor del precio base
                stock=random.randint(0, 100),  # Generando stocks aleatorios entre 0 y 100
                proveedor=proveedor,
                iva=random.randint(10, 20)  # Generando IVAs aleatorios entre 10 y 20
            )
            codigo += 1

    # Generando 5,000 órdenes de compra distribuidas en los últimos 365 días
    for i in range(5000):
        fecha_aleatoria = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))
        orden = Orden_Compra.objects.create(fecha=fecha_aleatoria)
        orden.fecha = fecha_aleatoria
        orden.save()

    productos = Productos.objects.all()
    ordenes_compra = Orden_Compra.objects.all()

    for orden in ordenes_compra:
        for _ in range(random.randint(1, 10)):  # Generando entre 1 y 10 productos por orden
            producto_aleatorio = random.choice(productos)
            cantidad_aleatoria = random.randint(1, 100)  # Generando cantidades aleatorias entre 1 y 100
            Orden_Productos.objects.create(
                orden=orden,
                nombre=producto_aleatorio.nombre,
                cantidad=cantidad_aleatoria
            )


def data_de_facturacion():

    Clientes.objects.all().delete()
    IdentificadorProductos.objects.all().delete()
    HistorialProductos.objects.all().delete()
    HistorialTipoDeCambio.objects.all().delete()
    Facturas.objects.all().delete()
    
    fake = Faker()

    # Crear clientes
    for _ in range(100):  # Ajusta el rango según cuántos clientes desees generar
        Clientes.objects.create(
            cedula=random.randint(10000000, 30000000),
            tipo=random.choice([0, 1]),
            nombre=fake.first_name(),
            apellido=fake.last_name()
        )

    productos_por_proveedor = {
        'FrutasFrescas': [('Manzana', 0.5), ('Banana', 0.3), ('Naranja', 0.6), ('Mango', 1), ('Melocotón', 1.2)],
        'Polar': [('Harina de Maiz', 1), ('Harina de Trigo', 1.1), ('Yogurt', 2), ('Granola', 3), ('Leche de Almendra', 3), ('Tofu', 2.5), ('Barra de Proteína', 1.5)],
        'Carnicería': [('Pechuga de Pollo', 5), ('Filete de Res', 7), ('Salchichas', 4), ('Pavo', 6), ('Chuleta de Cerdo', 5.5)],
        'TierraDeDulces': [('Chocolatina', 1), ('Gomitas', 0.5), ('Paleta', 0.25), ('Pastillas', 0.75), ('Chicle', 0.1)],
        'MercaditoElGocho': [('Espinaca', 2), ('Brocoli', 2.5), ('Zanahoria', 1.5), ('Lechuga', 1.5), ('Pepino', 1)],
        'MundoVinos': [('Merlot', 15), ('Chardonnay', 12), ('Pinot Noir', 20), ('Sauvignon Blanc', 18), ('Rosado', 15)],
        'Iberia': [('Sopa de Tomate', 3), ('Maíz Dulce', 2.5), ('Frijoles Negros', 2), ('Guisantes', 2), ('Atún', 2.5)],
        'SantaTeresa': [('Whisky', 25), ('Vodka', 20), ('Ron', 15), ('Ginebra', 20), ('Tequila', 25)]
    }

    codigo_producto = 1
    for productos in productos_por_proveedor.values():
        for producto in productos:
            nombre_producto, _ = producto
            IdentificadorProductos.objects.create(
                nombre=nombre_producto,
                codigo=codigo_producto
            )
            codigo_producto += 1
    
    # Crear historial de productos
    for _ in range(500):  # Ajusta el rango según cuántos productos desees generar
        product = random.choice(IdentificadorProductos.objects.all())
        HistorialProductos.objects.create(
            iva=random.randint(1, 20),
            precio=Decimal(random.uniform(1, 100)).quantize(Decimal("0.00")),
            cantidad=random.randint(1, 100),
            producto=product
        )

    # Crear historial de tipo de cambio
    for day in range(30):  # Ajusta el rango según cuántos días de historial de tipo de cambio desees generar
        HistorialTipoDeCambio.objects.create(
            cambio=Decimal(random.uniform(0.5, 1.5)).quantize(Decimal("0.0000")),
            fecha=fake.date_time_between(start_date='-30d', end_date='now')
        )

    # Crear facturas
    for _ in range(100):  # Ajusta el rango según cuántas facturas desees generar
        total_base = Decimal(random.uniform(10, 1000)).quantize(Decimal("0.00"))
        iva = Decimal(total_base * Decimal(0.12)).quantize(Decimal("0.00"))  # Suponiendo una tasa de IVA del 12%
        total = total_base + iva
        factura = Facturas.objects.create(
            fecha=fake.date_time_between(start_date='-30d', end_date='now'),
            total_base=total_base,
            iva=iva,
            total=total,
            id_cliente=random.choice(Clientes.objects.all()),
            id_tipo_de_cambio=random.choice(HistorialTipoDeCambio.objects.all()),
        )
        factura.productos.set(random.choices(HistorialProductos.objects.all(), k=random.randint(1, 5)))  # Ajusta el rango según cuántos productos por factura desees


def reporte_de_productos(request):
    # Productos más vendidos por proveedor
    proveedores = [
        'FrutasFrescas',
        'Polar',
        'Carnicería',
        'TierraDeDulces',
        'MercaditoElGocho',
        'MundoVinos',
        'Iberia',
        'SantaTeresa',
    ]

    meses = {
        1: 'Ene', 
        2: 'Feb', 
        3: 'Mar', 
        4: 'Abr', 
        5: 'May', 
        6: 'Jun', 
        7: 'Jul', 
        8: 'Ago', 
        9: 'Sep', 
        10: 'Oct', 
        11: 'Nov', 
        12: 'Dic'
    }
    
    # Crear un diccionario de nombres de productos y precios
    precios = Productos.objects.values_list('nombre', 'precio')
    precios_dict = {nombre: precio for nombre, precio in precios}

    # Producto más vendido
    producto_mas_vendido = Orden_Productos.objects.values('nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido').first()
    # Añadir el total monetario a la consulta del producto más vendido
    producto_mas_vendido['total_monetario'] = producto_mas_vendido['total_vendido'] * precios_dict[producto_mas_vendido['nombre']]

    # Productos más vendidos por proveedor
    productos_mas_vendidos_por_proveedor = []
    for proveedor in proveedores:
        # Buscar todos los productos de un proveedor
        productos = Productos.objects.filter(proveedor=proveedor).values_list('nombre', flat=True)
        
        # Buscar las ventas de estos productos
        producto_mas_vendido = Orden_Productos.objects.filter(nombre__in=productos).values('nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido').first()
        
        # Añadir el total monetario a la consulta del producto más vendido
        producto_mas_vendido['total_monetario'] = producto_mas_vendido['total_vendido'] * precios_dict[producto_mas_vendido['nombre']]
        producto_mas_vendido['proveedor'] = proveedor
        
        productos_mas_vendidos_por_proveedor.append(producto_mas_vendido)
    productos_mas_vendidos_por_proveedor = sorted(productos_mas_vendidos_por_proveedor, key=lambda x: x['total_vendido'], reverse=True)

    # Ventas por proveedor
    ventas_por_proveedor = []
    for proveedor in proveedores:
        # Buscar todos los productos de un proveedor
        productos = Productos.objects.filter(proveedor=proveedor).values_list('nombre', flat=True)
        
        # Sumar las ventas de estos productos
        total_vendido = Orden_Productos.objects.filter(nombre__in=productos).aggregate(total_vendido=Sum('cantidad'))['total_vendido']
        
        # Calcular el total monetario
        total_monetario = sum(cantidad * precios_dict[nombre] for nombre, cantidad in Orden_Productos.objects.filter(nombre__in=productos).values_list('nombre', 'cantidad'))
        
        ventas_por_proveedor.append({'proveedor': proveedor, 'total_vendido': total_vendido, 'total_monetario': total_monetario})

    # Subconsulta para obtener el precio del producto
    precio_producto = Productos.objects.filter(nombre=OuterRef('productos__nombre')).values('precio')

    # Consulta para obtener el total vendido y total monetario para cada mes
    ventas_por_mes = Orden_Compra.objects.annotate(
        mes=ExtractMonth('fecha'),
        year=ExtractYear('fecha')
    ).values('mes', 'year').annotate(
        total_vendido=Sum('productos__cantidad'),
        total_monetario=Sum(F('productos__cantidad') * Subquery(precio_producto[:1], output_field=DecimalField()))
    ).order_by('year', 'mes')

    # Para ventas por mes, también necesitamos añadir el total monetario.
    for venta in ventas_por_mes:
        venta['total_monetario'] = sum(
            cantidad * precios_dict[nombre] for nombre, cantidad in 
            Orden_Productos.objects.filter(
                orden__fecha__month=venta['mes']
            ).values_list('nombre', 'cantidad')
        )

    # Top 10 productos menos vendidos
    top_10_menos_vendidos = Orden_Productos.objects.values('nombre').annotate(total_vendido=Sum('cantidad')).order_by('total_vendido')[:10]
    # Añadir el total monetario a la consulta del top 10 de productos menos vendidos
    for producto in top_10_menos_vendidos:
        producto['total_monetario'] = producto['total_vendido'] * precios_dict[producto['nombre']]  

    clientes = Clientes.objects.annotate(total_compras=Count('facturas'))

    # Ordenar los clientes en orden descendente de 'total_compras'
    clientes = clientes.order_by('-total_compras').values('nombre', 'apellido', 'cedula', 'total_compras')
    top_clientes = clientes[:5]

    # Data de respaldo para las graficas
    proveedores = [venta['proveedor'] for venta in ventas_por_proveedor]
    totales_monetarios = [venta['total_monetario'] for venta in ventas_por_proveedor]
    totales_por_mes = [venta['total_monetario'] for venta in ventas_por_mes]
    for venta in ventas_por_mes:
        venta['mes'] = meses[venta['mes']]
    

    # Inicializar un diccionario vacío para almacenar los resultados
    analisis = {}
    
    # Obtener todos los productos únicos en el historial de productos
    productos = IdentificadorProductos.objects.all()
    
    for producto in productos:
        # Obtener todas las entradas de historial para este producto
        historial_producto = HistorialProductos.objects.filter(producto=producto)
        
        # Calcular la cantidad total vendida de este producto
        total_vendido = historial_producto.aggregate(Sum('cantidad'))['cantidad__sum']
        
        # Calcular el precio promedio de venta de este producto
        precio_promedio = historial_producto.aggregate(Avg('precio'))['precio__avg']
        
        # Agregar los resultados al diccionario de análisis
        analisis[producto.nombre] = {'nombre': producto.nombre, 'total_vendido': total_vendido, 'precio_promedio': precio_promedio}

    # Ordenar los productos por total vendido, en orden descendente
    productos_mas_vendidos = sorted(list(analisis.values()), key=lambda x: x['total_vendido'], reverse=True)
    # Ordenar los productos por total vendido, en orden ascendente
    productos_menos_vendidos = sorted(list(analisis.values()), key=lambda x: x['total_vendido'])

    print(Facturas.objects.aggregate(total=Sum('total')))
    return render(request, 'Reporte/productos.html', {
        'producto_mas_vendido': productos_mas_vendidos_por_proveedor,
        'productos_mas_vendidos_por_proveedor': productos_mas_vendidos_por_proveedor,
        'ventas_por_proveedor': ventas_por_proveedor,
        'ventas_por_mes': ventas_por_mes,
        'top_10_menos_vendidos': top_10_menos_vendidos,
        'proveedores': proveedores,
        'totales_monetarios': totales_monetarios,
        'totales_por_mes': totales_por_mes,
        'top_clientes': top_clientes,
        'analisis': analisis,
        'productos_mas_vendidos': productos_mas_vendidos,
        'productos_menos_vendidos': productos_menos_vendidos,
        'total_clientes': Clientes.objects.count(),
        'total_ventas': Facturas.objects.count(),
        'total_monto_ventas': round(Facturas.objects.aggregate(total=Sum('total'))['total'], 2),
        'total_productos': Productos.objects.count() 
    })