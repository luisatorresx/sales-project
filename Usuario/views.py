from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.models import User

def index(request):
    return render(request, 'Usuario/index_usuario.html')

def agregar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('lista_usuario')
        else:
            form.full_clean()
            return render(request, 'Usuario/agregar_usuario.html', {'form': form})
    else:
        form = UserForm()
        return render(request, 'Usuario/agregar_usuario.html', {'form': form})


def lista_usuario(request):
    users = User.objects.all()
    return render(request, 'Usuario/lista_usuario.html', {'users': users})
