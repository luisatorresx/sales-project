# Generated by Django 4.2.2 on 2023-07-21 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas', '0009_rename_total_cancelado_facturas_total_cancelado_en_bs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialtipodecambio',
            name='cambio',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=10),
        ),
    ]
