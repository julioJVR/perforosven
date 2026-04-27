# contabilidad/forms.py
from django import forms
from .models import CuentaContable, AsientoContable, MovimientoContable


class CuentaContableForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = ["codigo", "nombre", "descripcion", "tipo", "naturaleza", "nivel", "padre", "es_activo"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class AsientoContableForm(forms.ModelForm):
    class Meta:
        model = AsientoContable
        fields = ["numero", "fecha", "descripcion"]


class MovimientoContableForm(forms.ModelForm):
    class Meta:
        model = MovimientoContable
        fields = ["cuenta", "descripcion", "debe", "haber"]
