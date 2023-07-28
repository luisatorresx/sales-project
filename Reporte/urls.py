from django.urls import include, path
from . import views

urlpatterns = [
    path('productos/', views.reporte_de_productos ,name= "reporte_productos"),
]
