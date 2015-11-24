from django.conf.urls import url
from .views import *
from .reportes import generar_pdf_factura

urlpatterns = [
    url(r'^factura_venta/nueva/$', view_new_factura, name="nfactura_venta"),
    url(r'^factura_venta/$', view_facturas_venta, name="factura_venta"),
    url(r'^factura_venta/detalle/(?P<id_fv>\d+)/$', view_detalle_fv, name="detalle_fv"),
    url(r'^factura_venta/reporte/(?P<id>\d+)/$', generar_pdf_factura),

    url(r'^autorizaciones/$', view_autorizacion, name="autorizaciones"),
    url(r'^autorizaciones/nuevo/$', view_new_autorizacion, name="nautorizacion"),
    url(r'^autorizaciones/edit/(?P<pk>\d+)/$', view_edit_autorizacion, name="eautorizacion"),
    url(r'^autorizaciones/del/(?P<pk>\d+)/$', view_del_autorizacion, name="dautorizacion"),
    
 ]