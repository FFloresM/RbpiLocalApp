from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import *
from .forms import *

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
