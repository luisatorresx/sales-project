from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name= "index_inventario"),
    path('agregar_producto/', views.agregar_producto, name= "agregar_producto"),
    path('lista_productos/', views.lista_productos, name= "lista_productos"),
    path('reporte/', views.generar_reporte, name="generar_reporte"),
    path('actualizar_producto/', views.actualizar_producto, name="actualizar_producto"),
    path('error/', views.error, name="error"),
]
