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
    path('guardar_producto/<int:codigo>/', views.guardar_producto, name='guardar_producto'),
    path('orden_compra/', views.orden_compra, name='orden_compra'),
    path('quitar_producto/<str:nombre>/', views.quitar_producto, name='quitar_producto'),
    path('guardar_orden/', views.guardar_orden, name='guardar_orden'),
    path('historial_orden_compra/', views.historial_orden_compra, name='historial_orden_compra'),
    path('detalle_orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
]
