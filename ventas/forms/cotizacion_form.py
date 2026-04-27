from django import forms
from django.forms import inlineformset_factory

from ventas.models.cotizacion import Cotizacion
from ventas.models.detalle_cotizacion import DetalleCotizacion
from ventas.models.partida_contrato import PartidaContrato


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            "cliente", "contrato", "numero",
            "fecha", "fecha_servicio",
            "monto_total", "estado"
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={'type': 'date'}),
            "fecha_servicio": forms.DateInput(attrs={'type': 'date'}),
        }


class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = [
            "partida_contrato",
            "descripcion",
            "cantidad",
            "precio_unitario",
        ]


DetalleCotizacionFormSet = inlineformset_factory(
    Cotizacion,
    DetalleCotizacion,
    form=DetalleCotizacionForm,
    extra=1,
    can_delete=True
)
