from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name= "index_usuario"),
    path('agregar_usuario/', views.agregar_usuario, name= "agregar_usuario"),
    path('lista_usuario/', views.lista_usuario, name='lista_usuario'),
]

