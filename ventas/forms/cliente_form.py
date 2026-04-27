from django import forms
from ventas.models.cliente import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'tipo_documento',
            'rif',
            'nombre',
            'direccion',
            'telefono',
            'email',
            'activo'
        ]
