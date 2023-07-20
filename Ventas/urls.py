from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name= "ventas_index"),
    path('Facturacion/', views.facturacion, name= "facturacion"),
    path('Factura/<int:id>', views.factura, name="factura")
]