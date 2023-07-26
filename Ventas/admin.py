from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Clientes)
admin.site.register(models.HistorialProductos)
admin.site.register(models.Facturas)
admin.site.register(models.IdentificadorProductos)
admin.site.register(models.HistorialTipoDeCambio)