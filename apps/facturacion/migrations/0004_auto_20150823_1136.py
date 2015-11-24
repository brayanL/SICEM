# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0003_facturaventa_descuento_porcent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detallefv',
            old_name='fatura_venta',
            new_name='factura_venta',
        ),
    ]
