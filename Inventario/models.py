from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

def validate_unique_name(value):
    exists = Productos.objects.filter(name=value).exists()
    if exists:
        raise ValidationError('Este producto ya existe.')

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField(unique=True, validators=[validate_unique_name])
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.CharField(max_length=100)
    iva = models.IntegerField()

class Orden_Compra(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)

class Orden_Productos(models.Model):
    orden = models.ForeignKey(Orden_Compra, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
