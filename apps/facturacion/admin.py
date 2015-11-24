from django.contrib import admin
from .models import *

class DetalleFVInLine(admin.TabularInline):
    model = DetalleFV
    extra = 2

class FacturaVentaAdmin(admin.ModelAdmin):
    inlines = (DetalleFVInLine, )

admin.site.register(Autorizacion)
admin.site.register(FacturaVenta, FacturaVentaAdmin)