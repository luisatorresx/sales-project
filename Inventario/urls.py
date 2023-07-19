from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name= "index_inventario"),
    path('agregar_producto/', views.agregar_producto, name= "agregar_producto"),
    path('lista_productos/', views.lista_productos, name= "lista_productos"),
    path('reporte/', views.generar_reporte, name="generar_reporte"),
    path('error/', views.error, name="error"),
    path('borrar_producto/', views.borrar_producto, name="borrar_producto"),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('actualizar_producto/', views.actualizar_producto, name="actualizar_producto"),
    path('guardar_producto/<int:producto_id>/', views.guardar_producto, name='guardar_producto'),
]
