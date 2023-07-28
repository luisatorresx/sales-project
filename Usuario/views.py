from decimal import Decimal
from django.shortcuts import render, redirect

from Usuario.models import TipoDeCambio
from .forms import TipoDeCambioForm, UserForm, GroupForm, LoginForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

def index(request):
    
    if not (request.user.groups.filter(name='Administrador') or
            request.user.is_staff):
        return redirect('index')
    else:
        return render(request, 'Usuario/index_usuario.html')

def agregar_usuario(request):
    if not (request.user.groups.filter(name='Administrador') or
            request.user.is_staff):
        return redirect('index')

    if request.method == "POST":
        form = UserForm(request.POST)
        form2 = GroupForm(request.POST)
        if form.is_valid():
            print(request.POST)
            usuario = User.objects.create_user(**form.cleaned_data)
            usuario.groups.add(Group.objects.get(name=request.POST['rol']))
            return redirect('lista_usuario')
        else:
            form.full_clean()
            form2.full_clean()
            return render(request, 'Usuario/agregar_usuario.html', {'form': form, 'form2':form2})
    else:
        form2 = GroupForm()
        form = UserForm()
        return render(request, 'Usuario/agregar_usuario.html', {'form': form, 'form2':form2})


def lista_usuario(request):

    if not (request.user.groups.filter(name='Administrador') or
            request.user.is_staff):
        return redirect('index')
    print(request.POST)
    if request.method == "POST":
        if 'eliminar' in request.POST:
            u = User.objects.filter(username=request.POST['eliminar'])
            if u is not None:
                u.delete()
    
    users = list(User.objects.all())
    usuarios = []
    for user in users:
        usuarios.append([user,user.groups.first(),user.is_staff])

    return render(request, 'Usuario/lista_usuario.html', {'usuarios': usuarios})


def login_usuario(request):

    error = False
    if request.method == "POST":

        form = LoginForm(request.POST)
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = True
            return render(request, 'Usuario/login.html', {'form': form, 'error':error})
    else:
        form = LoginForm()
        return render(request, 'Usuario/login.html', {'form': form, 'error':error})


def logout_usuario(request):
    logout(request)
    return redirect('index')

def configuracion(request):
    
    actualizado = False
    es_0 = False

    if request.method == "POST":
        
        form = TipoDeCambioForm(request.POST)

        if form.is_valid():
            if Decimal(request.POST['cambio']) == Decimal(0.0000):
                es_0 = True
            else:
                cambio = TipoDeCambio.objects.first()
                cambio.cambio = request.POST['cambio']
                cambio.save()
                actualizado = True

        return render(request, 'Usuario/Configuración.html', {'form': form, 'actualizado':actualizado, 'es_0':es_0})
    else:
        
        if TipoDeCambio.objects.first() is not None:
            form = TipoDeCambioForm(initial={'cambio':TipoDeCambio.objects.first().cambio})
            if TipoDeCambio.objects.first().cambio == Decimal(0.0000):
                es_0 = True
        else:
            TipoDeCambio.objects.create()
            form = TipoDeCambioForm(initial={'cambio':TipoDeCambio.objects.first().cambio})
            es_0 = True

        return render(request, 'Usuario/Configuración.html', {'form': form, 'actualizado':actualizado, 'es_0':es_0})
