from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProductoForm
from .models import Productos, Orden_Compra, Orden_Productos


# Create your views here.
#Index
def index(request):
    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.groups.filter(name='Analista de datos') or
            request.user.is_staff):
        return redirect('index')
    
    return render(request, 'Inventario/index_inventario.html')

#Agrega un producto a la base de datos
def agregar_producto(request):

    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')
    
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Verificar si el producto ya existe en la base de datos
            codigo_producto = request.POST['codigo']
            if Productos.objects.filter(codigo=codigo_producto).exists():
                return render(request, 'Inventario/error.html')
                
            # Crear el nuevo producto si no existe
            else:
                Productos.objects.create(
                    nombre=request.POST['nombre'],
                    codigo=codigo_producto,
                    precio=request.POST['precio'],
                    stock=request.POST['stock'],
                    proveedor=request.POST['proveedor'],
                    iva=request.POST['iva']
                )
                return redirect('lista_productos')
        else:
            form.full_clean()
            return render(request, 'Inventario/agregar_producto.html', {'form': form})
    else:
        form = ProductoForm()
        return render(request, 'Inventario/agregar_producto.html', {'form': form})

#Muestra una lista con los productos
def lista_productos(request):

    filtro = request.GET.get('filtro')
    productos = Productos.objects.all()
    if filtro:
        productos = productos.filter(nombre__icontains=filtro)
    
    paginator = Paginator(productos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'Inventario/lista_productos.html', {'page_obj': page_obj, 'filtro': filtro})

#Muestra formularios con la informacion del producto a actualizar
def actualizar_producto(request):

    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')

    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            producto = get_object_or_404(Productos, codigo=codigo)
            producto.id


            form = ProductoForm(initial={'nombre': producto.nombre, 'codigo':producto.codigo, 'precio': producto.precio, 'stock':producto.stock,'proveedor':producto.proveedor, 'iva':producto.iva})
            return render(request, 'Inventario/actualizar_producto.html', {'id':producto.codigo, 'form':form})
        except:
            return render(request, 'Inventario/error.html')
    else:
        return render(request, 'Inventario/actualizar_producto.html')

#Sobreescribe la informacion en la base de datos (deberia hacer eso)
def guardar_producto(request, codigo):

    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')
    
    producto = get_object_or_404(Productos, codigo=codigo)
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.codigo = request.POST['codigo']
        producto.stock = request.POST['stock']
        producto.proveedor = request.POST['proveedor']
        producto.precio = request.POST['precio']
        producto.iva = request.POST['iva']
        producto.save()
        return redirect('lista_productos')

#Muestra la informacion del producto a eliminar
def borrar_producto(request):
    
    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')
    
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            producto = get_object_or_404(Productos, codigo=codigo)
            return render(request, 'Inventario/borrar_producto.html', {'producto': producto})
        except:
            return render(request, 'Inventario/error.html')

    return render(request, 'Inventario/borrar_producto.html')

#Elimina el producto de la base de dato
def eliminar_producto(request, producto_id):
    
    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')
    
    producto = get_object_or_404(Productos, id=producto_id)
    producto.delete()
    return redirect('lista_productos')

#Genera un reporte con toda la informacion de los items
def generar_reporte(request):

    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.groups.filter(name='Analista de datos') or
            request.user.is_staff):
        return redirect('index')
    
    productos = Productos.objects.all()
    # Renderizamos el template de confirmación
    return render(request, 'Inventario/reporte.html', {'productos': productos})

#View de errores
def error(request):
    return render(request, 'Inventario/error.html')

#Genera una orden de compra
productos = []
def orden_compra(request):
    
    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        
        if nombre and cantidad:
            productos.append({'nombre': nombre, 'cantidad': cantidad})
    
    return render(request, 'Inventario/orden_compra.html', {'productos': productos})

#Quita un producto de la orden de compra
def quitar_producto(request, nombre):

    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')
    
    for producto in productos:
        if producto['nombre'] == nombre:
            productos.remove(producto)
            break
    return redirect('orden_compra')


def guardar_orden(request):
    
    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')
    
    if request.method == 'POST':
        orden = Orden_Compra.objects.create()  # Crear una nueva instancia de Orden_Compra
        for producto in productos:
            orden_productos = Orden_Productos()
            orden_productos.orden = orden
            orden_productos.nombre = producto['nombre']
            orden_productos.cantidad = producto['cantidad']
            orden_productos.save()
        productos.clear()

        return redirect('historial_orden_compra')  # Redirigir a la nueva vista de tabla de órdenes de compra
    
    return redirect('index_inventario')

def historial_orden_compra(request):
    
    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.groups.filter(name='Analista de datos') or
            request.user.is_staff):
        return redirect('index')
    
    ordenes = Orden_Compra.objects.all()
    return render(request, 'Inventario/historial_orden_compra.html', {'ordenes': ordenes})


def detalle_orden(request, orden_id):

    if not (request.user.groups.filter(name='Administrador') or	
            request.user.groups.filter(name='Almacenista') or
            request.user.is_staff):
        return redirect('index')
    
    orden = Orden_Compra.objects.filter(id=orden_id).first()  # Obtener la orden de compra con el id proporcionado
    productos = Orden_Productos.objects.filter(orden=orden)  # Obtener los productos de esa orden de compra

    return render(request, 'Inventario/detalle_orden.html', {'orden': orden, 'productos': productos})
