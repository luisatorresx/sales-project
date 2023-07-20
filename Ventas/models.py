from django.db import models
from django.utils.timezone import now

# Create your models here.

class HistorialTipoDeCambio(models.Model):
    id = models.AutoField(primary_key=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    fecha = models.DateTimeField(default=now, editable=False)

class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido = models.CharField(max_length=30, blank=True, null=True)

class Facturas(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=now, editable=False)
    total_base = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    iva_total = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    abono_divisa = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    impuesto_divisa = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    total_cancelado = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_tipo_de_cambio = models.ForeignKey(HistorialTipoDeCambio, on_delete=models.CASCADE)

class IdentificadorProductos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()

class HistorialProductos(models.Model):
    id = models.AutoField(primary_key=True)
    iva = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    producto = models.ForeignKey(IdentificadorProductos, on_delete=models.CASCADE)
    factura = models.ManyToManyField(Facturas)