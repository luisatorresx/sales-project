from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= "index"),
    path('agregar_producto/', views.agregar_producto, name= "agregar_producto"),
    path('lista_productos/', views.lista_productos, name= "lista_productos")
]