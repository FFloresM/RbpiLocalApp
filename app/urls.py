from django.urls import path
from app.views import *

app_name = 'app'

urlpatterns = [
	path('', index, name='index'),
	path('pila/nueva', PilaCreate.as_view(), name='pila-nueva'),
	path('registros', RegistrosView.as_view(), name='registros'),

]