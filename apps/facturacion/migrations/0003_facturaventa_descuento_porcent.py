# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0002_auto_20150819_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturaventa',
            name='descuento_porcent',
            field=models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True),
        ),
    ]
