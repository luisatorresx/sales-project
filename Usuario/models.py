from django.db import models


# Create your models here.

class TipoDeCambio(models.Model):
    cambio = models.DecimalField(max_digits=10, decimal_places=4, default= 0.0000)
