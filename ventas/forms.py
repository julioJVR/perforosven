from django import forms
from .models.cliente import Cliente
from .models.contrato import Contrato
from django.contrib.auth.decorators import login_required


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_documento', 'rif', 'nombre',
            'direccion', 'telefono', 'email', 'activo'
        ]
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            'cliente', 'numero', 'objeto',
            'fecha_inicio', 'fecha_fin',
            'monto', 'estado', 'activo'
        ]
        widgets = {
            'objeto': forms.Textarea(attrs={'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

