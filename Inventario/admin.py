from django.contrib import admin
from Inventario.models import Productos, Orden_Compra, Orden_Productos

# Register your models here.
admin.site.register(Productos)
admin.site.register(Orden_Compra)
admin.site.register(Orden_Productos)
