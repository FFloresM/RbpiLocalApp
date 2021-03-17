from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors
#graphics
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.axes import YValueAxis

from datetime import datetime

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]
styles = getSampleStyleSheet()

hoy = datetime.today()

class PDF:
    def __init__(self, pila, cliente, lanza, mediciones):
        self.pila = pila
        self.cliente = cliente
        self.lanza = lanza
        self.mediciones = mediciones
        self.title = ""
        self.PageInfo = ""
    
    def setTitle(self, *args):
        self.title =  " ".join(args)

    def getTitle(self):
        return self.title

    def setPageInfo(self, *args):
        self.PageInfo = "pila "+"/".join(args)

    def getPageInfo(self):
        return self.PageInfo

    def Par(self, font_size, text):
        return Paragraph(f"""<font size={font_size}><b>{text}</b></font>""", styles["BodyText"])

    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold',16)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-50, self.getTitle())
        canvas.setFont('Times-Roman',9)
        canvas.drawString(0.5 * inch, 0.5 * inch, "1 %s" % self.getPageInfo())
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString(0.5 * inch, 0.5 * inch, "%d %s" % (doc.page, self.getPageInfo()))
        canvas.restoreState()

    def tableInfo(self):
        P = Image("../Pictures/FFV.png", width=100, height=100)
        data= [
            ['CLIENTE', 'LANZA', "Posición: sdfd\nPredio: 1234\nEstado: termofila\n\n\n", [P]],
            ['Nombre: {nombre}','Código: {codigo}',"",""],
            ['Email: {email}','Modelo: {modelo}',"",""],
            ['Dirección: {dirección}','Serie: {Serie}',"",""]
        ]
        tc=Table(data, colWidths=1.5*inch)
        tc.setStyle(TableStyle([
            ('TEXTCOLOR',(0,0),(1,-1),colors.black),
            ('GRID', (0,0), (-1,-1),1, colors.black),
            ('SPAN', (2,0),(2,3)),
            ('SPAN', (3,0),(3,3))
            ]))




#Title = "Reporte Pila {id_pila}"
#pageinfo = "pila {id_pila}/{cliente}/{serie_lanza}/"+hoy.strftime("%H:%M/%d-%m-%y")





materias_primas_data = [
	#[Par(13,"Materias Primas"),"",""],
	[Par(12,"Nombre"), Par(12,"cantidad"), Par(12,"Unidad de medida")],
	["mp1", "c1", "um1"],
	["mp2", "c2", "um2"]
]
mpt = Table(materias_primas_data, colWidths=2*inch)

data_mediciones = [
	#[Par(13,"Mediciones"),"",""],
	[Par(11,"Fecha"), Par(11,"Temperatura"), Par(11,"Humedad")],
	["f1","t1","h1"],
	["f2","t2","h2"],
	["f3","t3","h3"],	
	["f4","t4","h4"],
	["f5","t5","h5"]
]
medicionesTable = Table(data_mediciones, colWidths=2*inch)
medicionesTable.setStyle(TableStyle([
	('LINEBELOW', (0,0), (2,0), 1, colors.black),
	('LINEBELOW', (0,1), (-1,-1), 0.5, colors.black),
	]))

#chart
################################
drawing = Drawing(400, 200)
data = [((0.5,7), (1.5,1), (2.5,2), (3.5,1), (4.5,3), (5.5,5), (6.5, 10), (7.5,6))
        ]
bc = LinePlot()
bc.x = 50
bc.y = 50
bc.height = 125
bc.width = 300
bc.data = data

bc.xValueAxis.valueMin = 0
bc.xValueAxis.valueMax = 8
bc.xValueAxis.valueSteps = [1, 2, 2.5, 3, 4, 5, 6, 7]
bc.xValueAxis.labelTextFormat = '%2.1f'
bc.yValueAxis.valueMin = 0
bc.yValueAxis.valueMax = 10
#bc.yValueAxis.valueSteps = [1, 2, 3, 5, 6]
drawing.add(bc)

data3=[[(0.5, 4), (1.5, 3), (2.5, 4), (3.5, 6), (4.5, 4), (5.5, 2), (6.5, 5), (7.5, 6)]
       ]

lp = LinePlot()
lp.x = bc.x
lp.y = bc.y
lp.height = bc.height
lp.width = bc.width
lp.data = data3
lp.joinedLines = 1
lp.lines[0].symbol = makeMarker('Circle')
lp.lines[0].strokeColor=colors.blue
lp.lineLabelFormat = '%2.0f'
lp.xValueAxis.valueMin = 0
lp.xValueAxis.valueMax = len(data3[0])
lp.yValueAxis.valueMin = 0
lp.yValueAxis.valueMax = 8
lp.xValueAxis.visible=False
lp.yValueAxis.visible=False #Hide 2nd plot its Yaxis
drawing.add(lp)

y2Axis = YValueAxis()#Replicate 2nd plot Yaxis in the right
y2Axis.setProperties(lp.yValueAxis.getProperties())
y2Axis.setPosition(lp.x+lp.width,lp.y,lp.height)
y2Axis.tickRight=5
y2Axis.tickLeft=0
y2Axis.labels.dx = 10
y2Axis.configure(data3)
y2Axis.visible=True
drawing.add(y2Axis)

def go(buffer):
    doc = SimpleDocTemplate(buffer)#, "reporte.pdf")
    Story = [Spacer(0,0)]
    Story.append(tc)
    Story.append(Spacer(1,0.2*inch))
    Story.append(Par(13,"Materias Primas"))
    Story.append(Spacer(1,0.2*inch))
    Story.append(mpt)
    Story.append(Spacer(1,0.2*inch))
    Story.append(Par(13,"Mediciones"))
    Story.append(Spacer(1,0.2*inch))
    Story.append(medicionesTable)
    Story.append(Spacer(1,0.2*inch))
    Story.append(Par(13,"Gráfico"))
    Story.append(drawing)
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

if __name__ == "__main__":
    go()