from django.shortcuts import render, redirect
from .models import Autorizacion, FacturaVenta, DetalleFV, DetalleMovimiento
from apps.inventario.models import Producto
from .forms import AutorizacionForm
from apps.credito.models import SolicitudCredito
from django.contrib import messages
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import user_passes_test

from apps.reportes import generar_descargar_pdf
from .reportes import generar_pdf_factura


@permission_required('auth.add_facturaventa', raise_exception=True)
def view_new_factura(request):
    if request.method == "POST":
        #fact = None
        cli_email = None
        try:
            with transaction.atomic():
                fact = FacturaVenta.objects.create(autorizacion_sri_id=request.POST['id_autorizacion'],
                                                   empleado=request.user.empleado,
                                                   cliente_id=request.POST['id_cliente'],
                                                   subtotal=request.POST['subtotal'],
                                                   descuento=request.POST['descuento'],
                                                   descuento_porcent=request.POST['descuento_porcent'],
                                                   importe_iva_12=request.POST['iva'],
                                                   total=request.POST['total_cobrar']
                                                   )
                cli_email = fact.cliente.email
                list_detalle = str(request.POST['list_detalle']).split(",")
                for item in list_detalle:
                    id_in = "id"+item
                    prod = Producto.objects.get(pk=request.POST[id_in])
                    if prod.stock >= int(request.POST[('ca'+item)]):
                        prod.stock = int(prod.stock) - int(request.POST[('ca'+item)])
                        prod.save()
                        movi = DetalleMovimiento.objects.create(tipo=1,
                                                                producto=prod,
                                                                cantidad=int(request.POST[('ca'+item)]),
                                                                precio_unitario=float(request.POST[('pu'+item)]),
                                                                saldo_stock=prod.stock
                                                                )
                        DetalleFV.objects.create(movimiento=movi, factura_venta=fact)

                    else:
                        transaction.rollback()
                        messages.error(request, ("El stock se acaba de agotar para el producto: " + prod.nombre))
                        return redirect('/factura_venta/nueva/')
                if request.POST['fpago'] == 'Credito':
                    cred = SolicitudCredito.objects.create(factura_venta = fact,
                                                           garante_id=request.POST['id_garante'],
                                                           cant_letras=request.POST['cant_letras'],
                                                           cant_dinero=request.POST['cant_dinero'],
                                                           dia_vencimiento=request.POST['dia_vencimiento']
                                                           )

                #generar_descargar_pdf('facJota.pdf', )
                messages.success(request, "Se realizó con éxtio total la factura.")
                print ('llegue 011111')

                print ('llegue 022222')
        except Exception as error:
            print(error)
            transaction.rollback()
            messages.error(request, ("Comuniquese con Soporte técnico. "+ str(error)))
            return redirect('/factura_venta/nueva/')
        try:
            if cli_email is not None:
                print (fact.id)
                enviar_mail(request, cli_email, generar_pdf_factura(request, fact.id))
        except Exception as e:
            messages.error(request, ("Error al Enviar el Correo al Cliente. "+ str(e)))
        return redirect('/factura_venta/nueva/')
    else:
        auto = "Agregue una autorización"
        if Autorizacion.objects.count() == 0:
            messages.warning(request, "Debe ingresar una autorización"
                                      " y luego recargar la pagina para grabar la facutra.")
        else:
            auto = Autorizacion.objects.last()
        nro_fact = FacturaVenta.objects.count() + 1
        return render(request, "nueva_factura.html", {"auto": auto, "nro_fact": nro_fact})


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def view_facturas_venta(request):
    fventa = FacturaVenta.objects.all()
    return render(request, "facturas_venta.html", {"fventa": fventa})


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def view_detalle_fv(request, id_fv):
    detalle = FacturaVenta.objects.get(pk=id_fv).detallefv_set.all()
    print("DEtalle: ", detalle)
    return render(request, "detalle_fventa.html", {"detalle":detalle})

def enviar_mail(request, cli_email, contenido):
    print(cli_email)
    mail = EmailMessage(subject="Generacion de Factura",from_email='Jose Eras <jogaec22@gmail.com>',
                            to=['jogaec22@gmail.com'])
    mail.template_name = 'FacturaVenta'

    mail.attach('factuJose.pdf', contenido.getvalue(), 'application/pdf')
    mail.send()


@permission_required('auth.add_autorizacion', raise_exception=True)
def view_new_autorizacion(request):
    if request.method == "POST":
        mfautorizacion = AutorizacionForm(request.POST)
        if mfautorizacion.is_valid():
            mfautorizacion.save()
            messages.success(request, "La Autorización fue creado con éxito.")
            return redirect("/autorizaciones/nuevo/")
    else:
        mfautorizacion = AutorizacionForm()
    return render(request, "nueva_autorizacion.html", {"form": mfautorizacion})


@permission_required('auth.del_autorizacion', raise_exception=True)
def view_autorizacion(request):
    autorizaciones = Autorizacion.objects.all()
    return render(request, "autorizaciones.html", {"autorizaciones": autorizaciones})


@permission_required('auth.change_autorizacion', raise_exception=True)
def view_edit_autorizacion(request, pk):
    if request.method == "POST":
        mfautorizacion = AutorizacionForm(request.POST, instance=Autorizacion.objects.get(pk=pk))
        if mfautorizacion.is_valid():
            mfautorizacion.save()
            messages.info(request, "Se han guardado los cambios con éxito.")
            return redirect('/autorizaciones/edit/'+pk)
        else:
            messages.warning(request, "No olvide llenar todos los campos obligatorios e ingresar datos correctos.")
    else:
        mfautorizacion = AutorizacionForm(instance=Autorizacion.objects.get(pk=pk))
    return render(request, "edit_autorizacion.html", {"form": mfautorizacion})


@permission_required('auth.del_autorizacion', raise_exception=True)
def view_del_autorizacion(request, pk):
    if request.method == "POST":
        try:
            Autorizacion.objects.get(pk=pk).delete()
            messages.success(request, "La autorización ID=" + pk + " fue eliminado con éxito")
        except Exception as error:
            messages.error(request, "No se puede eliminar por que se esta usando actualmente.")
        return redirect('/autorizaciones/')

