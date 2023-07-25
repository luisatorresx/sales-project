# Generated by Django 4.2.1 on 2023-07-24 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0004_alter_productos_iva'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orden_Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orden_Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField()),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='Inventario.orden_compra')),
            ],
        ),
    ]