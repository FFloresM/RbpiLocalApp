from django.urls import path
from app.views import *

app_name = 'app'

urlpatterns = [
	path('', index, name='index'),
	path('pila/nueva', PilaCreate.as_view(), name='pila-nueva'),
	path('pila/<int:pk>/eliminar', PilaDelete.as_view(), name='pila-delete'),
	path('pila/<int:pk>/editar', PilaUpdate.as_view(), name='pila-update'),
	path('materia-prima/agregar', MateriaPrimaCreate.as_view(), name='materia-prima-nueva'),
	path('predio/agregar', PredioCreate.as_view(), name='predio-nuevo'),

	path('registros', RegistrosView.as_view(), name='registros'),
	path('registros/<int:pk>', medicionesPila, name='mediciones-pila'),

	path('chart/<int:pk>', chart, name='chart'),
	path('chart', allCharts, name='all-charts'),

	path('reporte/<int:pk>', pdf_test, name='pdf'),

]