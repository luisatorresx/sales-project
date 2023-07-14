from django.db import models

# Create your models here.

class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)

class Facturas(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    total_base = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    iva_total = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    abono_divisa = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    impuesto_divisa = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    total_cancelado = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)

class IdentificadorProductos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()

class HistorialProductos(models.Model):
    id = models.AutoField(primary_key=True)
    iva = models.BooleanField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    producto = models.ForeignKey(IdentificadorProductos, on_delete=models.CASCADE)
    factura = models.ManyToManyField(Facturas)