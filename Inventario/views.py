from django.shortcuts import render, redirect
from .forms import ProductoForm
from .models import Productos

# Create your views here.

def index(request):
    return render(request, 'index.html')


def agregar_producto(request):
    #Agregamos un producto
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            Productos.objects.create(nombre= request.POST['nombre'], codigo= request.POST['codigo'], precio= request.POST['precio'], stock= request.POST['stock'])
            return redirect('lista_productos')
    
    else:
        form = ProductoForm()
        return render(request, 'agregar_producto.html', {'form': form})


def lista_productos(request):
    #Buscamos todos los productos
    productos = Productos.objects.all()

    #Mostrar la lista con todos los productos
    return render(request, 'lista_productos.html', {'productos': productos})


def actualizar_producto(request, codigo_producto):
    # Buscamos el producto que queremos actualizar
    producto = Productos.objects.get(codigo_producto= codigo_producto)

    # Cargamos la información en un formulario
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    # Renderizamos el template con el formulario
    return render(request, 'actualizar_producto.html', {'form': form, 'codigo_producto': codigo_producto})


def borrar_producto(request, codigo_producto):
    # Buscamos el producto que queremos eliminar
    producto = Product.objects.get(codigo_producto= codigo_producto)

    # Si se ha enviado el formulario de confirmación, eliminamos el producto
    if request.method == 'POST':
        product.delete()
        return redirect('lista_productos')

    # Renderizamos el template de confirmación
    return render(request, 'borrar_producto.html', {'product': product})