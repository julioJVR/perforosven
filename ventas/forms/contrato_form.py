from django import forms
from django.forms import inlineformset_factory
from ventas.models.contrato import Contrato
from ventas.models.partida_contrato import PartidaContrato


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = [
            "cliente", "numero", "descripcion",
            "fecha_inicio", "fecha_fin",
            "monto_total", "activo"
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
            "fecha_inicio": forms.DateInput(attrs={"type": "date"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date"}),
        }


class PartidaContratoForm(forms.ModelForm):
    class Meta:
        model = PartidaContrato
        fields = ["descripcion", "monto"]


PartidaContratoFormSet = inlineformset_factory(
    Contrato,
    PartidaContrato,
    form=PartidaContratoForm,
    extra=1,
    can_delete=True
)
