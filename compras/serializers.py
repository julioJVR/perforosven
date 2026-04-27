# compras/serializers.py
from rest_framework import serializers
from .models import Factura, Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'codigo_proveedor', 'rif', 'nombre_empresa']

class FacturaSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(read_only=True)
    proveedor_id = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all(), source='proveedor', write_only=True)

    class Meta:
        model = Factura
        fields = [
            'id', 'proveedor', 'proveedor_id', 'orden_compra', 'fecha_factura', 'fecha_registro',
            'descripcion_servicio', 'numero_factura', 'numero_control', 'soporte_documento',
            'moneda', 'monto_base', 'aplica_iva', 'iva', 'total_factura', 'municipio',
            'porcentaje_ret_iva', 'porcentaje_ret_islr', 'porcentaje_ret_municipal',
            'ret_iva', 'ret_islr', 'ret_municipal', 'tasa_cambio'
        ]
        read_only_fields = ['iva', 'total_factura', 'ret_iva', 'ret_islr', 'ret_municipal', 'fecha_registro']

    def validate_monto_base(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto base debe ser mayor que cero.")
        return value

    def create(self, validated_data):
        # validated_data contiene 'proveedor' (objeto) por el field write_only proveedor_id
        factura = Factura(**validated_data)
        # calcular montos automáticamente usando el método del modelo
        factura.save()
        return factura

    def update(self, instance, validated_data):
        # actualizar campos y recalcular
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
