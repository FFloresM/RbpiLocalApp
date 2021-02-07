from django.forms import ModelForm, TextInput, Select
from .models import Pila


class PilaCreateForm(ModelForm):
	class Meta:
		model = Pila
		fields = ['nombreID', 'predio', 'estado', 'cliente']
		widgets = {
			'nombreID': TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Pila'}),
			'predio': TextInput(attrs={'class':'form-control', 'placeholder':'Predio'}),
			'estado': TextInput(attrs={'class':'form-control', 'placeholder':'Estado'}),
			'cliente': Select(attrs={'class':'form-control'}),
		}

class PilaUpdateForm(ModelForm):
	class Meta:
		model = Pila
		fields = ['nombreID', 'predio', 'estado']
		widgets = {
			'nombreID': TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Pila'}),
			'predio': TextInput(attrs={'class':'form-control', 'placeholder':'Predio'}),
			'estado': TextInput(attrs={'class':'form-control', 'placeholder':'Estado'}),
		}

