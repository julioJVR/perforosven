# Repositorio simple para aisentar dependencias de data-access
from .models import AsientoContable, MovimientoContable, CuentaContable
from django.shortcuts import get_object_or_404


class AsientoRepository:
    @staticmethod
    def crear_asiento(fecha, descripcion, referencia=None, origen=None, origen_id=None):
        a = AsientoContable.objects.create(
        fecha=fecha, descripcion=descripcion, referencia=referencia, origen=origen, origen_id=origen_id
        )
        return a


class MovimientoRepository:
    @staticmethod
    def crear_movimiento(asiento, cuenta_codigo_or_obj, descripcion, debe=0, haber=0):
        # aceptar cuenta por código o por instancia
        if isinstance(cuenta_codigo_or_obj, CuentaContable):
            cuenta = cuenta_codigo_or_obj
        else:
            cuenta = get_object_or_404(CuentaContable, codigo=cuenta_codigo_or_obj)
        linea = MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuenta,
            detalle=descripcion,
            debe=debe or 0,
            haber=haber or 0
            )
        return linea