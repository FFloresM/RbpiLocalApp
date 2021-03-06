import io
from django.http import FileResponse
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from reportlab.lib import colors
from .models import *
from .forms import *
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter, A4

def index(request):
	cliente = Cliente.objects.get(id=1)
	lanzas = Lanza.objects.all()
	pilas = Pila.objects.all()
	context = {
		'cliente': cliente,
		'lanzas': lanzas,
		'pilas': pilas,
	}
	return render(request, 'app/index.html', context)

class PilaCreate(CreateView):
	model = Pila
	form_class = PilaCreateForm

	def get_success_url(self):
		return reverse('app:index')

class PilaDelete(DeleteView):
	model = Pila
	success_url = reverse_lazy('app:index')

class PilaUpdate(UpdateView):
	model = Pila
	form_class = PilaUpdateForm
	template_name = 'app/pila_update.html'
	success_url = reverse_lazy('app:index')

class MateriaPrimaCreate(CreateView):
	model = MateriaPrima
	form_class = MateriaPrimaCreateForm
	success_url = reverse_lazy('app:index')

def medicionesPila(request, pk):
	pila = Pila.objects.get(id=pk)
	query = Medicion.objects.filter(pila=pila)
	materia_prima = MateriaPrima.objects.filter(pila=pila)
	context = {
		'registros': query,
		'pila': pila,
		'materia_prima': materia_prima,
	}
	return render(request, 'app/mediciones_pila.html', context)
	


class RegistrosView(generic.ListView):
	model = Medicion
	context_object_name = 'mediciones'
	#nueva consulta
	#queryset = Medicion.objects.filter()
	template_name = 'app/registros.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = timezone.now()
		context['pilas'] = Pila.objects.all()
		return context

def chart(request, pk):
	mediciones = Medicion.objects.filter(pila__id=pk)
	pila = Pila.objects.get(id=pk)
	temps = mediciones.values_list('temperatura', flat=True)
	dates = mediciones.values_list('fecha_creacion', flat=True)
	dias = [date.day for date in dates ]
	humedad = mediciones.values_list('humedad', flat=True)
	context = {
		'pila': pila,
		'temps': list(temps),
		'dias': dias,
		'dates': dates,
		'humedad': list(humedad),
	}
	return render(request, 'app/chart_pila.html', context)

def allCharts(request):
	mediciones = Medicion.objects.all()
	context = {
		'mediciones': mediciones,
	}
	return render(request, 'app/chart.html', context)

def pdf_test(request, pk):
	#queries for models
	mediciones = Medicion.objects.filter(pila__id=pk)
	pila = Pila.objects.get(id=pk)
	# Create a file-like buffer to receive PDF data.
	buffer = io.BytesIO()

	# Create the PDF object, using the buffer as its "file."
	p = canvas.Canvas(buffer, pagesize=letter)
	title = f'Reporte Pila {pila.nombreID}'
	p.setTitle(title)

	width, height = letter 
	#tabla
	#data = [['1','2','3'],
	#		['4','5','6']]
	#t = Table(data)
	#t.setStyle(TableStyle([('BACKGROUND', (1,1), (-2,-2), colors.green)]))
	#w, h = t.wrapOn(p,400,100)
	
	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	p.drawString(100, 100, "Hello world.")
	p.drawCentredString(100, height-10, title)

	lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris commodo rutrum libero eget posuere. Pellentesque ornare dignissim ante ut finibus. Curabitur id massa sit amet elit sagittis euismod sed sit amet ex. Morbi mauris felis, pulvinar eget est in, sodales bibendum quam. Aenean in arcu et arcu consectetur rutrum. Aliquam tellus arcu, auctor eu lacus sed, tempus accumsan tortor. Etiam rutrum, ante quis condimentum laoreet, nunc sapien accumsan nibh, sit amet aliquet dui ligula tincidunt dui. Ut pretium, massa nec egestas maximus, mauris leo sagittis diam, ac ullamcorper mi odio a ipsum. Vivamus imperdiet pharetra tellus, ac porttitor magna ornare nec. Nulla facilisi. Interdum et malesuada fames ac ante ipsum primis in faucibus."

	p.drawCentredString(100,700, lorem)


    # Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	#nombre de reporte
	
	return FileResponse(buffer, as_attachment=False, filename='reporte.pdf')
