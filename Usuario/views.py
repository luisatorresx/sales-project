from django.shortcuts import render, redirect
from .forms import UserForm, GroupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'Usuario/index_usuario.html')

def agregar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        form2 = GroupForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
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
