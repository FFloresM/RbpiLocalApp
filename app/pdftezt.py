from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors
#graphics
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.axes import YValueAxis
from reportlab.graphics.charts.textlabels import Label

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

def setTitle(title):
    global Title
    Title = title

def setPageInfo(page_info):
    global pageinfo
    pageinfo = page_info

def Par(font_size, text):
	return Paragraph(f"""<font size={font_size}><b>{text}</b></font>""", styles["BodyText"])

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-50, Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(0.5 * inch, 0.5 * inch, "1/%s" % pageinfo)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(0.5 * inch, 0.5 * inch, "%d %s" % (doc.page, pageinfo))
    canvas.restoreState()

data = [["","","",""],["","","",""],["","","",""],["","","",""]]
def setDataFirstTable(cliente, lanza, url):
    global data
    P = Image(url, width=130, height=100)
    data= [
        ['CLIENTE', 'LANZA',[P]],
        [f'Nombre:\n{cliente.nombre}',f'Código: {lanza.codigo}',""],#,""],
        [f'Email:\n{cliente.email}',f'Modelo: {lanza.modelo}',""],#,""],
        [f'Dirección:\n{cliente.direccion}',f'Serie: {lanza.numero_serie}',""],#,""]
    ]

def getFirstTable():
    tc=Table(data, colWidths=2*inch)
    tc.setStyle(TableStyle([
        ('TEXTCOLOR',(0,0),(1,-1),colors.black),
        ('GRID', (0,0), (-1,-1),1, colors.black),
        ('SPAN', (2,0),(2,3)),
        ]))
    return tc

def setDetallePila(pila):
    global detallePila
    detallePila = Paragraph(
        f"""<b>Posición:</b> <a href="https://www.google.cl/maps/@-36.8174503,-73.0423481,14.21z">{pila.posicion}</a>\t <b>Predio:</b> {pila.predio} \t<b>Último estado:</b> {pila.estado}""", 
        styles["BodyText"]
        )

def getDetallePila():
    return detallePila

def setMateriasPrimas(materiaprima):
    global materias_primas_data
    materias_primas_data = [
        [Par(12,"Nombre"), Par(12,"cantidad"), Par(12,"Unidad de medida")],
    ]
    for m in materiaprima:
        m = list(m)
        materias_primas_data.append(m[1:-1])

def getMPTable():
    return Table(materias_primas_data, colWidths=2*inch)

def setDataMediciones(mediciones):
    global data_mediciones
    data_mediciones = [
        [Par(11,"Fecha"), Par(11,"Temperatura"), Par(11,"Humedad")],
    ]
    i = 1
    for m in mediciones:
        m = list(m[1:-2])
        m[0] = m[0].strftime("%d-%m-%Y")
        data_mediciones.append(m)
        i=i+1



def getTablaMediciones():
    medicionesTable = Table(data_mediciones, colWidths=2*inch)
    medicionesTable.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (2,0), 1, colors.black),
        ('LINEBELOW', (0,1), (-1,-1), 0.5, colors.black),
        ]))
    return medicionesTable

#chart
################################
def setTemps(temperaturas):
    global temps
    temps = temperaturas

def getTemps():
    return temps

def setHumedad(humedades):
    global humedad
    humedad = humedades

def getHumedad():
    return humedad

def getPlot():
    drawing = Drawing(400, 200)
    #temps = [((0.5,7), (1.5,1), (2.5,2), (3.5,1), (4.5,3), (5.5,5), (6.5, 10), (7.5,6))]
    temps = [getTemps()]
    bc = LinePlot()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = temps
    #labels
    yilabel = Label()
    yilabel.setText("Temperatura (°C)")
    yilabel.angle = 90
    yilabel.setOrigin(20,120)
    xlabel = Label()
    xlabel.setText("Días")
    xlabel.setOrigin(200,20)

    labelT = Label()
    labelT.setText("Temperatura")
    labelT.setOrigin(210,185)

    labelH = Label()
    labelH.setText("Humedad")
    labelH.setOrigin(285,185)


    bc.xValueAxis.valueMin = 0
    bc.xValueAxis.valueMax = 20
    bc.xValueAxis.valueSteps = [x for x in range(1,bc.xValueAxis.valueMax)]
    #bc.xValueAxis.labelTextFormat = '%2.1f'
    bc.yValueAxis.valueMin = 0
    bc.yValueAxis.valueMax = 60
    bc.yValueAxis.valueSteps = [0, 10, 20, 30, 40, 50, 60]
    drawing.add(bc)
    drawing.add(yilabel)
    drawing.add(xlabel)
    drawing.add(Line(170,185,185,185, strokeColor=colors.red))
    drawing.add(Line(250,185,265,185, strokeColor=colors.blue))
    drawing.add(labelT)
    drawing.add(labelH)

    #humedad=[[(0.5, 4), (1.5, 3), (2.5, 4), (3.5, 6), (4.5, 4), (5.5, 2), (6.5, 5), (7.5, 6)]]
    humedad = [getHumedad()]
    lp = LinePlot()
    lp.x = bc.x
    lp.y = bc.y
    lp.height = bc.height
    lp.width = bc.width
    lp.data = humedad

    ydlabel = Label()
    ydlabel.setText("Humedad (%)")
    ydlabel.angle = -90
    ydlabel.setOrigin(lp.x+lp.width+30,lp.y+70)

    lp.joinedLines = 1
    lp.lines[0].symbol = makeMarker('Circle')
    lp.lines[0].strokeColor=colors.blue
    lp.lineLabelFormat = '%2.0f'
    lp.xValueAxis.valueMin = 0
    lp.xValueAxis.valueMax = bc.xValueAxis.valueMax
    lp.yValueAxis.valueMin = 0
    lp.yValueAxis.valueMax = 100
    lp.xValueAxis.visible=False
    lp.yValueAxis.visible=False #Hide 2nd plot its Yaxis
    drawing.add(lp)
    drawing.add(ydlabel)

    y2Axis = YValueAxis()#Replicate 2nd plot Yaxis in the right
    y2Axis.setProperties(lp.yValueAxis.getProperties())
    y2Axis.setPosition(lp.x+lp.width,lp.y,lp.height)
    y2Axis.tickRight=5
    y2Axis.tickLeft=0
    y2Axis.labels.dx = 20
    y2Axis.configure(humedad)
    y2Axis.visible=True
    drawing.add(y2Axis)

    return drawing

def go(buffer):
    doc = SimpleDocTemplate(buffer)#, "reporte.pdf")
    Story = [Spacer(0,0)]
    Story.append(getFirstTable())
    Story.append(Spacer(1,0.2*inch))
    Story.append(getDetallePila())
    Story.append(Spacer(1,0.2*inch))
    Story.append(Par(13,"Materias Primas"))
    Story.append(Spacer(1,0.2*inch))
    Story.append(getMPTable())
    Story.append(Spacer(1,0.2*inch))
    Story.append(Par(13,"Mediciones"))
    Story.append(Spacer(1,0.2*inch))
    Story.append(getTablaMediciones())
    Story.append(Spacer(1,0.2*inch))
    Story.append(Par(13,"Gráfico"))
    Story.append(getPlot())
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

if __name__ == "__main__":
    go()