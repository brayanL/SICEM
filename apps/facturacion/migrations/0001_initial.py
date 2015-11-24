# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('actores', '0001_initial'),
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autorizacion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('autorizacion_sri', models.CharField(max_length=200)),
                ('nro_establecimiento', models.PositiveIntegerField()),
                ('nro_emision', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleFV',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FacturaVenta',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('graba_iva_12', models.DecimalField(blank=True, max_digits=8, decimal_places=2, null=True)),
                ('graba_iva_0', models.DecimalField(blank=True, max_digits=8, decimal_places=2, null=True)),
                ('subtotal', models.DecimalField(blank=True, max_digits=8, decimal_places=2, null=True)),
                ('descuento', models.DecimalField(blank=True, max_digits=8, decimal_places=2, null=True)),
                ('importe_iva_12', models.DecimalField(blank=True, max_digits=8, decimal_places=2, null=True)),
                ('total', models.DecimalField(blank=True, max_digits=9, decimal_places=2, null=True)),
                ('autorizacion_sri', models.ForeignKey(to='facturacion.Autorizacion')),
                ('cliente', models.ForeignKey(to='actores.Cliente')),
                ('empleado', models.ForeignKey(to='actores.Empleado')),
            ],
        ),
        migrations.AddField(
            model_name='detallefv',
            name='fatura_venta',
            field=models.ForeignKey(to='facturacion.FacturaVenta'),
        ),
        migrations.AddField(
            model_name='detallefv',
            name='movimiento',
            field=models.OneToOneField(to='inventario.DetalleMovimiento'),
        ),
    ]
