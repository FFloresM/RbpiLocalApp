from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def index(request):
	cliente = Cliente.objects.all()
	context = {'cliente': cliente}
	return render(request, 'base.html', context)

