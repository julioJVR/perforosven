# compras/api/serializers.py
from rest_framework import serializers
from compras.models import Factura
from compras.models import Proveedor


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'rif', 'nombre_empresa']


class FacturaSerializer(serializers.ModelSerializer):
    proveedor_detail = ProveedorSerializer(source='proveedor', read_only=True)
    rif_proveedor = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Factura
        fields = [
            'id', 'proveedor', 'proveedor_detail', 'rif_proveedor', 'orden_compra', 'fecha_factura',
            'descripcion_servicio', 'numero_factura', 'numero_control', 'soporte_documento',
            'moneda', 'monto_base', 'tasa_cambio', 'tiene_iva', 'alicuota_iva',
            'porcentaje_ret_iva', 'porcentaje_ret_islr', 'porcentaje_ret_municipal',
            'ret_iva', 'ret_islr', 'ret_municipal', 'iva', 'total_factura', 'municipio'
        ]
        read_only_fields = ['ret_iva', 'ret_islr', 'ret_municipal', 'iva', 'total_factura']
