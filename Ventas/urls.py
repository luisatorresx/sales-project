from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name= "index"),
    path('Facturacion/', views.facturacion, name= "facturacion"),
    #path('FacturaAImprimir/', views.FacturaAImprimir, name= "FacturaAImprimir")
]