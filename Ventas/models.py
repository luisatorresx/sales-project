from django.db import models
from django.utils.timezone import now

# Create your models here.

class HistorialTipoDeCambio(models.Model):
    id = models.BigAutoField(primary_key=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=4, default= 0.0000)
    fecha = models.DateTimeField(default=now, editable=False)

class Clientes(models.Model):
    id = models.BigAutoField(primary_key=True)
    cedula = models.IntegerField(unique=True)
    tipo = models.IntegerField(default=0)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido = models.CharField(max_length=30, blank=True, null=True)

class IdentificadorProductos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()

class HistorialProductos(models.Model):
    id = models.BigAutoField(primary_key=True)
    iva = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    cantidad = models.IntegerField(default=0)
    producto = models.ForeignKey(IdentificadorProductos, on_delete=models.CASCADE)

class Facturas(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(default=now, editable=False)
    total_base = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    cancelado_en_divisa = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    impuesto_divisa = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    cancelado_en_bs = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    vuelto = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_tipo_de_cambio = models.ForeignKey(HistorialTipoDeCambio, on_delete=models.CASCADE)
    productos = models.ManyToManyField(HistorialProductos)
    