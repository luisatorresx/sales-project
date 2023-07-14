from django.shortcuts import render, redirect
from django.core.paginator import Paginator
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
    
    paginator = Paginator(productos, 3)  # Divide los productos en páginas de 3 elementos por página
    page_number = request.GET.get('page')  # Obtiene el número de página actual desde la query string
    page_obj = paginator.get_page(page_number)  # Obtiene el objeto Page correspondiente a la página actual
    
    return render(request, 'Inventario/lista_productos.html', {'page_obj': page_obj, 'filtro': filtro})


def actualizar_producto(request, codigo=None):
    if codigo:
        producto = Productos.objects.get(codigo=codigo)
        if request.method == 'POST':
            form = ProductoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                return redirect('lista_productos')
        else:
            form = ProductoForm(instance=producto)
    else:
        form = ProductoForm()

    return render(request, 'Inventario/actualizar_producto.html', {'form': form, 'codigo': codigo})


def borrar_producto(request, codigo):
    # Buscamos el producto que queremos eliminar
    producto = Productos.objects.get(codigo= codigo)

    # Si se ha enviado el formulario de confirmación, eliminamos el producto
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')

    # Renderizamos el template de confirmación
    return render(request, 'Inventario/borrar_producto.html', {'producto': producto})


def generar_reporte(request):
    productos = Productos.objects.all()
    # Renderizamos el template de confirmación
    return render(request, 'Inventario/reporte.html', {'productos': productos})