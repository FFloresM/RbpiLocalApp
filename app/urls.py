from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
	path('', views.index, name='index'),
	path('nueva', views.nuevaPila, name='nueva'),
	path('registros', views.RegistrosView.as_view(), name='registros'),

]