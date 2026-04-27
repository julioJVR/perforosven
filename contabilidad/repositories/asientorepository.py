# contabilidad/repositories/asiento_repository.py
from ..models import AsientoContable, MovimientoContable, CuentaContable
from django.db import transaction
from decimal import Decimal

class AsientoRepository:
    @staticmethod
    def crear_asiento(fecha, descripcion, referencia=None, origen=None, origen_id=None):
        asiento = AsientoContable.objects.create(
            fecha=fecha,
            descripcion=descripcion,
            referencia=referencia,
            origen=origen,
            origen_id=origen_id
        )
        return asiento

class MovimientoRepository:
    @staticmethod
    def crear_movimiento(asiento, cuenta_codigo, descripcion, debe=0, haber=0):
        # buscar cuenta por código; si no existe, lanza excepción para que el proceso lo registre
        cuenta = CuentaContable.objects.filter(codigo=cuenta_codigo).first()
        if not cuenta:
            raise Exception(f"Cuenta con código {cuenta_codigo} no encontrada (crear en plan de cuentas).")
        return MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuenta,
            detalle=descripcion,
            debe=Decimal(debe or 0),
            haber=Decimal(haber or 0)
        )
