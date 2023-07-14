# Generated by Django 4.2.2 on 2023-07-14 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas', '0003_remove_facturas_total_facturas_abono_divisa_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialTipoDeCambio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cambio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fecha', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='clientes',
            name='nombreCompelto',
        ),
        migrations.AddField(
            model_name='clientes',
            name='apellido',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='clientes',
            name='nombre',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='cedula',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ventas.historialtipodecambio'),
        ),
    ]
