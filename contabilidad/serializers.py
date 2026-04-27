from rest_framework import serializers
from .models import CuentaContable, AsientoContable, MovimientoContable


class CuentaContableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaContable
        fields = '__all__'


class MovimientoContableSerializer(serializers.ModelSerializer):
    cuenta_codigo = serializers.CharField(source='cuenta.codigo', read_only=True)
    cuenta_nombre = serializers.CharField(source='cuenta.nombre', read_only=True)

    class Meta:
        model = MovimientoContable
        fields = [
            'id',
            'cuenta',
            'cuenta_codigo',
            'cuenta_nombre',
            'debe',
            'haber'
        ]


class AsientoContableSerializer(serializers.ModelSerializer):
    movimientos = MovimientoContableSerializer(many=True)

    class Meta:
        model = AsientoContable
        fields = [
            'id',
            'fecha',
            'descripcion',
            'movimientos'
        ]

    def create(self, validated_data):
        movimientos_data = validated_data.pop('movimientos')
        asiento = AsientoContable.objects.create(**validated_data)

        for mov in movimientos_data:
            MovimientoContable.objects.create(asiento=asiento, **mov)

        return asiento
