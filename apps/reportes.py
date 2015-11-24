#Para los reportes

from io import BytesIO
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, TableStyle, Image, Spacer, Paragraph, BaseDocTemplate, PageTemplate
from reportlab.lib import colors
from reportlab.platypus import Table, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_LEFT
from reportlab.lib.pagesizes import A4, letter, A5, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
#from flask import make_response
from django.core.mail import EmailMessage


def __encabezado(canvas, fuentes, size, x, y, listPosLogo):
    canvas.saveState()

    xx=0
    if x[7] == '/':
        xx = inch/x[0]
    else:
        xx = inch+x[0]
    canvas.drawImage("apps/inicio/static/sbadmin/img/cmz2.png", xx, y[0],
                     width=listPosLogo[0],
                     height=listPosLogo[1])
    canvas.setFont(fuentes['HelveticaBold'], size[0])
    canvas.drawString(inch + x[1], y[1], """Casa Musical "ZAMBRANO" """)

    canvas.setFont(fuentes['TimesRoman'], size[1])
    canvas.drawString(inch + x[2], y[2], "Carlos Humberto Zambrano")

    canvas.setFont(fuentes['TimesRoman'], size[2])
    canvas.drawString(inch + x[3], y[3], "Distribuidores de Instrumentos Musicales%s"%size[6])

    canvas.setFont(fuentes['TimesRoman'], size[3])
    canvas.drawString(inch + x[4], y[4], "CREDITO Y OFERTAS")

    canvas.setFont(fuentes['TimesRoman'], size[4])
    canvas.drawString(inch + x[5], y[5], "Direccion: Junin 1217 e/. Rocafuerte y Bolivar - "
                                                       "Telef.: 937-105-937-717 ")
    canvas.setFont(fuentes['TimesBold'], size[5])
    canvas.drawString(inch + x[6], y[6], "MACHALA - EL ORO - ECUADOR")

    canvas.restoreState()


def __encabezado_A5_Vertical(canvas, doc):
    listFuentes = {'HelveticaBold': 'Helvetica-Bold', 'TimesRoman': 'Times-Roman', 'TimesBold': 'Times-Bold'}
    listFontSize = [14, 14, 7, 13, 8, 6, ', Electrodomesticos y Articulos de Bazar en General']
    listPosX = [5, 8, 32, -42, 18, -30, 38, '/']
    listPosY = [A5[1]-65, A5[1]-24, A5[1]-38, A5[1]-46, A5[1]-58, A5[1]-67, A5[1]-75]
    listPosLogo = [82, 54]
    __encabezado(canvas, listFuentes, listFontSize, listPosX, listPosY, listPosLogo)


def __encabezado_A5_Horizontal(canvas, doc):
    listFuentes = {'HelveticaBold':'Helvetica-Bold', 'TimesRoman':'Times-Roman','TimesBold':'Times-Bold'}
    listFontSize = [20, 20, 11, 18, 10, 8, ' y Electrodomesticos']
    listPosX = [3, 23, 52,-12,30,-17,63, '/']
    listPosY = [A5[1]-279, A5[1]-224, A5[1]-242, A5[1]-256, A5[1]-274, A5[1]-284, A5[1]-294]
    listPosLogo = [90,70]
    __encabezado(canvas, listFuentes, listFontSize, listPosX, listPosY, listPosLogo)


def __encabezado_A4_Vertical(canvas, doc):
    listFuentes = {'HelveticaBold':'Helvetica-Bold', 'TimesRoman':'Times-Roman','TimesBold':'Times-Bold'}
    listFontSize = [16, 14, 10, 12, 9, 8, ' y Electrodomesticos']
    listPosX = [50, 128, 145, 98, 150, 85, 155, '+']
    listPosY = [A4[1]-80, A4[1]-30, A4[1]-44, A4[1]-55, A4[1]-68, A4[1]-78, A4[1]-88]
    listPosLogo = [90,70]
    __encabezado(canvas, listFuentes, listFontSize, listPosX, listPosY, listPosLogo)



def generar_pdf(doc, elementsFilaPage):
    response = HttpResponse(content_type='application/pdf')
    return __generar_pdf_general(response, doc, elementsFilaPage)


def generar_descargar_pdf(pdf_name, doc, elementsFilaPage):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    #response['Content-Disposition'] = 'filename=%s'%pdf_name
    return __generar_pdf_general(response, doc, elementsFilaPage)


def __generar_pdf_general(response, docParametros, elementsFilaPage):
    buff = BytesIO()

    # frame_A4_Vertical = Frame(inch/3, inch/3, 555, 805, id='normal', showBoundary=0)
    # Frame_A5_Horizontal = Frame(inch/2, 20, 530, 375, id='a5', showBoundary=0)
    # Frame_A5_vertical = Frame(inch/3, inch/3, 384, 562, id='a5', showBoundary=0)
    doc = BaseDocTemplate(buff, pagesize=docParametros['pagesize'], title=docParametros['title'])
    if (docParametros['pagesize'] == A4 and docParametros['title'] not in 'Reporte Kardex'):
        print ("a4 v")
        doc.addPageTemplates([
            PageTemplate(id='cabecera', frames=Frame(inch/3, inch/3, 555, 805, id='normal', showBoundary=0),
                         onPage=__encabezado_A4_Vertical),
        ]
        )
    elif (docParametros['pagesize'] == landscape(A5)):
        print ("a5 h")
        doc.addPageTemplates([
            PageTemplate(id='cabecera', frames=Frame(inch/2, 20, 530, 375, id='a5', showBoundary=0),
                         onPage=__encabezado_A5_Horizontal),
        ]
        )
    elif (docParametros['pagesize'] == A5):
        print ("a5 v")
        doc.addPageTemplates([
            PageTemplate(id='cabecera', frames=Frame(inch/3, inch/3, 384, 562, id='a5', showBoundary=0),
                         onPage=__encabezado_A5_Vertical),
        ]
        )
    else:
        print ('cualquier papel sin encabezado')
        doc = SimpleDocTemplate(buff, pagesize=docParametros['pagesize'], rightMargin=20, leftMargin=20, topMargin=20,
                                bottomMargin=20, showBoundary=0,
                                title=docParametros['title'],)

    story = []
    #story.append(Spacer(0, 50))

    for i in elementsFilaPage:
         story.append(i)

    doc.build(story)
    response.write(buff.getvalue())
    #response.write()
    #mail.attach('factuJose.pdf', buff.getvalue(), 'application/pdf')
    #mail.send()
    buff.close()
    return response


def getDocumentoPlantilla(papel, title):
    docParametros = {'pagesize': papel, 'title': title}
    return docParametros


def estiloTablas(t):
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))



def enviar_mail(request, cli_email):
    print(cli_email)
    mail = EmailMessage(subject="Generacion de Factura",from_email='Brayan Loayza <godsarmybl@gmail.com>',
                            to=[cli_email])
    mail.template_name = 'FacturaVenta'

    mail.attach_file()
    mail.send()
#def generar_pdf(bf, doc, elementsFilaPage):
#    pass
