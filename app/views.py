from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone
from .models import *

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

def nuevaPila(request):
	
	return render(request, 'app/nueva_pila.html')

"""
def registros(request):

	return render(request, 'app/registros.html')
"""
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
