from django.db import models

# Create your models here.
class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.IntegerField()
    nombreCompelto = models.CharField(max_length=100)
    

class Facturas(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    total = models.IntegerField()
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)


class IdentificadorProductos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()

class HistorialProductos(models.Model):
    id = models.AutoField(primary_key=True)
    iva = models.BooleanField()
    precio = models.IntegerField()
    producto = models.ForeignKey(IdentificadorProductos, on_delete=models.CASCADE)
    factura = models.ManyToManyField(Facturas)