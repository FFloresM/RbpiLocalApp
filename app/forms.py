from django.forms import ModelForm, TextInput, Select, NumberInput
from .models import MateriaPrima, Pila


class PilaCreateForm(ModelForm):
	class Meta:
		model = Pila
		fields = ['nombreID', 'predio', 'cliente']
		widgets = {
			'nombreID': TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Pila'}),
			'predio': Select(attrs={'class':'form-control'}),
			#'estado': Select(attrs={'class':'form-control', 'placeholder':'Estado'}),
			'cliente': Select(attrs={'class':'form-control'}),
		}

class PilaUpdateForm(ModelForm):
	class Meta:
		model = Pila
		fields = ['nombreID', 'predio']#, 'estado']
		widgets = {
			'nombreID': TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Pila'}),
			'predio': Select(attrs={'class':'form-control', 'placeholder':'Predio'}),
			#'estado': Select(attrs={'class':'form-control', 'placeholder':'Estado'}),
		}

class MateriaPrimaCreateForm(ModelForm):
	class Meta:
		model = MateriaPrima
		fields = ['nombre', 'cantidad', 'unidad_medida', 'pila']
		widgets = {
			'nombre': TextInput(attrs={'class':'form-control', 'placeholder':'Nombre materia prima'}),
			'cantidad': NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad materia prima'}),
			'unidad_medida': TextInput(attrs={'class':'form-control', 'placeholder':'Unidad de medida'}),
			'pila': Select(attrs={'class':'form-control'}),
		}

