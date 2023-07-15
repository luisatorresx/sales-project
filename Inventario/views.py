from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProductoForm
from .models import Productos

# Create your views here.

def index(request):
    return render(request, 'Inventario/index_inventario.html')


def agregar_producto(request):
    #Agregamos un producto
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


def lista_productos(request):
    filtro = request.GET.get('filtro')
    productos = Productos.objects.all()

    # Aplica el filtrado si el parámetro de filtro está presente
    if filtro:
        productos = productos.filter(nombre__icontains=filtro)  # Filtra por coincidencia parcial de nombre
    
    paginator = Paginator(productos, 6)  # Divide los productos en páginas de 6 elementos por página
    page_number = request.GET.get('page')  # Obtiene el número de página actual desde la query string
    page_obj = paginator.get_page(page_number)  # Obtiene el objeto Page correspondiente a la página actual
    
    return render(request, 'Inventario/lista_productos.html', {'page_obj': page_obj, 'filtro': filtro})


def actualizar_producto(request):

    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            producto = get_object_or_404(Productos, codigo=codigo)
        except:
            return render(request, 'Inventario/error.html')
        form = ProductoForm(initial={
            'nombre': producto.nombre,
            'codigo': producto.codigo,
            'precio': producto.precio,
            'stock': producto.stock,
            'proveedor': producto.proveedor
        })

        if form.is_valid():
            # Actualizar los valores del producto con los nuevos valores del formulario
            producto.__dict__.update(form.cleaned_data)
            producto.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'Inventario/actualizar_producto.html', {'form': form})


def borrar_producto(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            producto = get_object_or_404(Productos, codigo=codigo)
            return render(request, 'Inventario/borrar_producto.html', {'producto': producto})
        except:
            return render(request, 'Inventario/error.html')

    return render(request, 'Inventario/borrar_producto.html')


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    producto.delete()
    return redirect('lista_productos')


def generar_reporte(request):
    productos = Productos.objects.all()
    # Renderizamos el template de confirmación
    return render(request, 'Inventario/reporte.html', {'productos': productos})

def error(request):
    return render(request, 'Inventario/error.html')
