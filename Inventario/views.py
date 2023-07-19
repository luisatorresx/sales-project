from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProductoForm
from .models import Productos

# Create your views here.
#Index
def index(request):
    return render(request, 'Inventario/index_inventario.html')

#Agrega un producto a la base de datos
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            Productos.objects.create(
                nombre= request.POST['nombre'],
                codigo= request.POST['codigo'],
                precio= request.POST['precio'],
                stock= request.POST['stock'],
                proveedor= request.POST['proveedor']
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
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            producto = get_object_or_404(Productos, codigo=codigo)
            return render(request, 'Inventario/actualizar_producto.html', {'producto':producto})
        except:
            return render(request, 'Inventario/error.html')

    else:
        form = ProductoForm()

    return render(request, 'Inventario/actualizar_producto.html')

#Sobreescribe la informacion en la base de datos (deberia hacer eso)
def guardar_producto(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.codigo = request.POST['codigo']
        producto.stock = request.POST['stock']
        producto.proveedor = request.POST['proveedor']
        producto.precio = request.POST['precio']
        producto.save()
        return redirect('lista_productos')

#Muestra la informacion del producto a eliminar
def borrar_producto(request):
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
    producto = get_object_or_404(Productos, id=producto_id)
    producto.delete()
    return redirect('lista_productos')

#Genera un reporte con toda la informacion de los items
def generar_reporte(request):
    productos = Productos.objects.all()
    # Renderizamos el template de confirmación
    return render(request, 'Inventario/reporte.html', {'productos': productos})

#View de errores
def error(request):
    return render(request, 'Inventario/error.html')
