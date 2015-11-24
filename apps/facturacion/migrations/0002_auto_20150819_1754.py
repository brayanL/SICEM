# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturaventa',
            name='graba_iva_0',
        ),
        migrations.RemoveField(
            model_name='facturaventa',
            name='graba_iva_12',
        ),
    ]
