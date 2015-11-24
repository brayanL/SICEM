
from .models import FacturaVenta
from io import BytesIO
from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Image, Spacer, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter, A5, landscape
from reportlab.platypus import Table
from apps.reportes import generar_pdf, generar_descargar_pdf, getDocumentoPlantilla, estiloTablas

from .models import FacturaVenta, DetalleFV

import time

fechaSistema = time.strftime("%d/%m/%y").split('/')

def generar_pdf_factura(request, id):
    doc = getDocumentoPlantilla(A5, 'Reporte Factura')

    styles = getSampleStyleSheet()
    estilo = styles['Heading6']
    estilo.fontSize = 6

    factura = FacturaVenta.objects.get(pk=id)
    story = []
    story.append(Spacer(0, 56))
    story.append(Paragraph(("&nbsp;" * 43) + "OBLIGADO A LLEVAR CONTABILIDAD", estilo))



    #####################################   TABLA RUC DE LA EMPRESA   #########################################
    story.append(Spacer(0, -76))
    ruc = Table(
        data=[
            [' ' * 148, 'R.U.C. 0700690399001 '],
        ], rowHeights=10)
    ruc.setStyle([
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('FONT', (0, 0), (0, 0), 'Times-Roman'),
        ('BOTTOMPADDING', (1, 0), (1, -0), -2),
        ('GRID', (1, 0), (1, 0), 1, colors.black),
        # ('BACKGROUND', (1, 1), (1, 1), colors.dodgerblue)
    ])
    story.append(ruc)

    ruc = Table(
        data=[
            [' ' * 93, '  F A C T U R A  '],
        ], rowHeights=13)
    ruc.setStyle([
        ('FONTSIZE', (1, 1), (-1, -1), 12),
        ('FONT', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (1, -1), (-1, -1), 1),
        ('GRID', (1, 0), (1, -1), 1, colors.black),
        ('BACKGROUND', (1, 0), (1, 0), colors.darkgray),
    ])
    story.append(ruc)






    ###########################################   SERIE  ########################################################
    story.append(Spacer(0, -2))
    estilo.fontSize = 7
    story.append(Paragraph(("&nbsp;" * 155) + "Serie %s-%s-"%(factura.autorizacion_sri.nro_establecimiento,
                                                              factura.autorizacion_sri.nro_emision), estilo))





    #######################################   NUMERO SECUENCIAL DE LA FACTURA ####################################
    estilo.fontSize = 13
    numeros = 0
    ceros = ''
    if len(str(factura.id)) < 9:
        for i in range(0, (9 - len(str(factura.id)))):
            ceros+='0'
    story.append(Paragraph(("&nbsp;" * 80) + "%s" % (ceros+str(factura.id)), estilo))






    #######################   PEQUEÑA TABLA DEL SRI Y FECHA DE EMISION DE LA FACTURA   #########################
    story.append(Spacer(0, 12))
    sriFecha = Table([
        ['', 'AUT. SRI. %s'%factura.autorizacion_sri.autorizacion_sri],
    ], colWidths=[270, 90], rowHeights=10)
    sriFecha.setStyle([
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (1, 0), (1, 0), -3),
        ('GRID', (1, 0), (-1, 0), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('BACKGROUND', (1, 0), (1, 0), colors.dodgerblue),
    ])
    story.append(sriFecha)

    sriFecha = Table([
        ['', 'DIA', 'MES', 'AÑO'],
        ['', '%s'%fechaSistema[0], '%s'%fechaSistema[1], '%s'%fechaSistema[2]],
    ], colWidths=[270, 30, 30, 30], rowHeights=12)
    story.append(Spacer(0, 3))
    sriFecha.setStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONT', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (1, 0), (-1, -1), -1),
        ('GRID', (1, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (1, 0), (-1, 0), colors.darkgray),
    ])
    story.append(sriFecha)





    ########################################  CABECERA DE LA FACTURA   #########################################
    story.append(Spacer(0, -15))
    estilo.fontSize = 5
    cabecera = Table([
        ['Señores:', '%s %s' % (factura.cliente.nombres, factura.cliente.apellidos)],
        ['Direccion:', '%s' % (factura.cliente.direccion)],
        ['R.U.C./C.I.: ', '%s' % (factura.cliente.cedula_ruc)],
        ['Formas de Pago:', '%s                Telef.: %s' % ('', factura.cliente.telefono)]
        # , '%s'%(factura.cliente.telefono)],
    ], colWidths=[66, 308], rowHeights=[16, 16, 16, 22])
    cabecera.setStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONT', (0, 0), (0, -1), 'Times-Bold'),
        ('FONT', (1, 0), (1, 2), 'Times-Roman'),
        ('FONT', (1, 3), (1, 3), 'Times-Bold'),
        # LEFTPADDING
        # RIGHTPADDING
        ('LEFTPADDING', (1, 3), (1, 3), 0),
        # ('FONT', (3, -1), (3, -1), 'Times-Roman'),
        # ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    story.append(cabecera)




    ####################################   DETALLE DE LA FACTURA   ##############################################
    alldetalles = [(d.movimiento.cantidad,
                    d.movimiento.producto,
                    d.movimiento.precio_unitario,
                    (d.movimiento.cantidad * d.movimiento.precio_unitario)) for d in factura.detallefv_set.all()]
    # aux = 0
    # if len(alldetalles) <= 14:
    #     aux = 0#14-len(alldetalles)
    detalle = Table([
        ('CANT.', 'DESCRIPCION', 'P. UNITARIO', 'IMPORTE'),
    ] +alldetalles+['']*(18-len(alldetalles)), colWidths=[32, 224, 60, 68], rowHeights=16)

    detalle.setStyle([
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('GRID', (0, 0), (4, -1), 1, colors.black),
        # ('BACKGROUND', (1, 1), (1, -1), colors.dodgerblue)
    ])
    story.append(detalle)





    #############################   SUBTOTALES,  DESCUENTO, IVA, TOTAL Y FIRMA   ##############################
    totales = Table([
        ['', 'SUB-TOTAL $', '%s'%(factura.subtotal)],
        ['', 'DESCUENTO $', '%s'%(factura.descuento)],
        ['', 'IMPORTE 12% IVA$ $', '%s'%(factura.importe_iva_12)],
        [('     ' + '_' * 20 + ' ' * 24 + '_' * 20
          + '\n' + ' ' * 11 + 'F. AUTORIZADA' + ' ' * 38 + 'F. CLIENTE'),
         'TOTAL A COBRAR $', '%s'%(factura.total)],
    ], colWidths=[244, 72, 68], rowHeights=[18, 18, 18, 24])
    totales.setStyle([
        ('FONTSIZE', (0, 0), (1, 3), 6),
        ('FONTSIZE', (2, 0), (2, 3), 8),
        # ('FONT', (0, 0), (-1, -1), 'Times-Bold'),
        # ('FONT', (0, 1), (0, 1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, 3), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('GRID', (1, 0), (-1, 3), 1, colors.black),
        # ('GRID', (0, 3), (-1, 3), 1, colors.black),
        # ('BACKGROUND', (1, 1), (1, -1), colors.dodgerblue)
    ])
    story.append(totales)


    ##################################### RETORNAR RESPONSE PDF   ##############################################
    #generar_pdf(doc, story)[1].close()
    return generar_pdf(doc, story)
    #return generar_descargar_pdf('factuJose.pdf', doc, story)
