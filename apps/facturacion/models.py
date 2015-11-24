from django.db import models
from apps.actores.models import Empleado, Cliente
from apps.inventario.models import DetalleMovimiento
from django.utils import timezone


class Autorizacion(models.Model):
    autorizacion_sri = models.CharField(max_length=200)
    nro_establecimiento = models.PositiveIntegerField()
    nro_emision = models.PositiveIntegerField()

    def __str__(self):
        return "%d - %d - %s" % (self.nro_emision, self.nro_establecimiento, self.autorizacion_sri)


class FacturaVenta(models.Model):
    autorizacion_sri = models.ForeignKey(Autorizacion)
    empleado = models.ForeignKey(Empleado)
    fecha = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente)
    subtotal = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    descuento = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    descuento_porcent = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    importe_iva_12 = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)
    total = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2)

    def __str__(self):
        return "%s - %s" % (self.cliente, self.fecha)


class DetalleFV(models.Model):
    movimiento = models.OneToOneField(DetalleMovimiento)
    factura_venta = models.ForeignKey(FacturaVenta)
