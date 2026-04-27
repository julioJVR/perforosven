# compras/forms.py
from django import forms
from django.forms import HiddenInput
from decimal import Decimal
from .models import Proveedor, Producto, OrdenCompra, Factura

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['rif', 'nombre_empresa', 'direccion', 'telefono', 'correo', 'activo',
                  'representante_nombre', 'representante_cedula', 'representante_telefono', 'representante_correo',
                  'banco_nacional', 'cuenta_nacional', 'tipo_cuenta_nacional',
                  'banco_extranjero', 'cuenta_extranjera', 'swift']
        widgets = {
            'rif': forms.TextInput(attrs={'class': 'w-full border rounded p-2', 'placeholder': 'Ej: J-12345678-9'}),
            # ... otros widgets ...
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'descripcion', 'unidad_medida', 'precio_unitario']

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'total']

class FacturaForm(forms.ModelForm):
    # campo para teclear RIF visible
    rif_proveedor = forms.CharField(label="RIF del Proveedor", required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border rounded p-2', 'placeholder': 'Ej: J-12345678-9', 'autocomplete': 'off'
    }))

    # checkbox IVA visible (no-mapped)
    aplica_iva = forms.BooleanField(label='Aplica IVA (16%)', required=False, initial=True)

    # porcentajes de retención que usuario ingresará
    ret_iva_pct = forms.DecimalField(label='Retención IVA (%)', required=False, initial=Decimal('0.00'),
                                    min_value=Decimal('0.00'), max_value=Decimal('100.00'),
                                    widget=forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'step': '0.01'}))
    ret_islr_pct = forms.DecimalField(label='Retención ISLR (%)', required=False, initial=Decimal('0.00'),
                                     min_value=Decimal('0.00'), max_value=Decimal('100.00'),
                                     widget=forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'step': '0.01'}))
    ret_municipal_pct = forms.DecimalField(label='Retención Municipal (%)', required=False, initial=Decimal('0.00'),
                                           min_value=Decimal('0.00'), max_value=Decimal('100.00'),
                                           widget=forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'step': '0.01'}))

    class Meta:
        model = Factura
        fields = ['proveedor', 'orden_compra', 'fecha_factura',
                  'descripcion_servicio', 'numero_factura', 'numero_control',
                  'soporte_documento', 'moneda', 'monto_base', 'tasa_cambio', 'municipio',
                  'iva', 'total_factura', 'ret_iva', 'ret_islr',
                  'porcentaje_ret_municipal', 'ret_municipal']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'orden_compra': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'fecha_factura': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded p-2'}),
            'descripcion_servicio': forms.Textarea(attrs={'class': 'w-full border rounded p-2', 'rows': 3}),
            'numero_factura': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'numero_control': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),
            'soporte_documento': forms.Textarea(attrs={'class': 'w-full border rounded p-2', 'rows': 2}),
            'moneda': forms.Select(attrs={'class': 'w-full border rounded p-2'}),
            'monto_base': forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'step': '0.01'}),
            'tasa_cambio': forms.NumberInput(attrs={'class': 'w-full border rounded p-2', 'step': '0.01'}),
            'municipio': forms.TextInput(attrs={'class': 'w-full border rounded p-2'}),

            # Hidden fields filled by JS but available to be submitted
            'iva': HiddenInput(),
            'total_factura': HiddenInput(),
            'ret_iva': HiddenInput(),
            'ret_islr': HiddenInput(),
            'porcentaje_ret_municipal': HiddenInput(),
            'ret_municipal': HiddenInput(),
        }

    def clean(self):
        cleaned = super().clean()
        monto_base = cleaned.get('monto_base') or Decimal('0.00')
        ret_mun_pct = cleaned.get('ret_municipal_pct') or Decimal('0.00')
        if monto_base <= 0:
            raise forms.ValidationError("El monto base debe ser mayor que cero.")
        if ret_mun_pct < 0 or ret_mun_pct > 100:
            raise forms.ValidationError("El porcentaje de retención municipal debe estar entre 0 y 100.")
        return cleaned
