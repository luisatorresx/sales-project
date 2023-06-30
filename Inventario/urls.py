from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name= "index"),
    path('agregar_producto/', views.agregar_producto, name= "agregar_producto"),
    path('lista_productos/', views.lista_productos, name= "lista_productos"),
    path('generar_reporte/', views.generar_reporte, name='generar_reporte')
]
