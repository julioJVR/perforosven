from django import forms
from ventas.models import DetalleCotizacion

class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = ['descripcion', 'cantidad', 'precio_unitario']
