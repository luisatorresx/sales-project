# Generated by Django 4.2.2 on 2023-07-23 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas', '0003_historialproductos_total_producto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historialproductos',
            name='total_producto',
        ),
    ]