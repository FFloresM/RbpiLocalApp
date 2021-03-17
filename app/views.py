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
from .pdftezt import *
from datetime import datetime


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
	mediciones = Medicion.objects.filter(pila__id=pk).values_list()
	pila = Pila.objects.get(id=pk)
	cliente = Cliente.objects.get(id=pila.cliente_id)
	lanza = Lanza.objects.get(cliente=cliente)
	materiaprima = MateriaPrima.objects.filter(pila = pila).values_list()
	# Create a file-like buffer to receive PDF data.
	buffer = io.BytesIO()
	hoy = datetime.today()
	#datos y funciones para generar pdf
	title = f"Reporte Pila {pila.nombreID}"
	setTitle(title)
	pageinfo = f"pila-{pila.nombreID}/{cliente.nombre}/{lanza.numero_serie}/"+hoy.strftime("%H:%M/%d-%m-%y")
	setPageInfo(pageinfo)
	setDataFirstTable(cliente, lanza, pila.foto.file.name)
	setDetallePila(pila)
	setMateriasPrimas(materiaprima)
	setDataMediciones(mediciones)
	temps = list(mediciones.values_list('temperatura', flat=True))
	setTemps(temps)
	humedad = list(mediciones.values_list('humedad', flat=True))
	setHumedad(humedad)
	# Create the PDF object, using the buffer as its "file."
	go(buffer)

	# FileResponse sets the Content-Disposition header so that browsers
	# present the option to save the file.
	buffer.seek(0)
	#nombre de reporte
	
	return FileResponse(buffer, as_attachment=False, filename='reporte.pdf')
