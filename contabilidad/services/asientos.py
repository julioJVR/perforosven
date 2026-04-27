# contabilidad/services/asientos.py
from datetime import datetime
from decimal import Decimal
from ..repositories import AsientoRepository, MovimientoRepository

def generar_asiento_desde_factura(factura):
    """
    Genera asiento contable a partir de una factura de compras (VEN-NIIF baseline).
    Usar repositorios para persistencia.
    """
    descripcion = f"Asiento por factura Nº {factura.numero_factura} - Proveedor {getattr(factura.proveedor, 'nombre_empresa', '')}"
    asiento = AsientoRepository.crear_asiento(
        fecha=factura.fecha_factura or datetime.now().date(),
        descripcion=descripcion,
        referencia=f"FAC-{factura.id}",
        origen="COMPRAS",
        origen_id=factura.id
    )

    # Mapeo de cuentas por defecto (debes parametrizar en DB si lo deseas)
    CUENTA_GASTO = "5-01-01"           # ejemplo
    CUENTA_IVA_CRED_FISCAL = "1-03-05"
    CUENTA_RET_IVA = "2-02-01"
    CUENTA_RET_ISLR = "2-02-02"
    CUENTA_RET_MUNIC = "2-02-03"
    CUENTA_POR_PAGAR = "2-01-01"

    # Debe: gasto
    MovimientoRepository.crear_movimiento(
        asiento=asiento,
        cuenta_codigo=CUENTA_GASTO,
        descripcion="Gasto/Servicio adquirido",
        debe=Decimal(factura.monto_base),
        haber=Decimal('0.00')
    )

    # Debe: IVA si hay
    if getattr(factura, 'iva', 0) and Decimal(factura.iva) > 0:
        MovimientoRepository.crear_movimiento(
            asiento=asiento,
            cuenta_codigo=CUENTA_IVA_CRED_FISCAL,
            descripcion="Crédito fiscal IVA",
            debe=Decimal(factura.iva),
            haber=Decimal('0.00')
        )

    # Haber: retenciones y proveedor
    if getattr(factura, 'ret_iva', 0) and Decimal(factura.ret_iva) > 0:
        MovimientoRepository.crear_movimiento(
            asiento=asiento,
            cuenta_codigo=CUENTA_RET_IVA,
            descripcion="Retención IVA",
            debe=Decimal('0.00'),
            haber=Decimal(factura.ret_iva)
        )

    if getattr(factura, 'ret_islr', 0) and Decimal(factura.ret_islr) > 0:
        MovimientoRepository.crear_movimiento(
            asiento=asiento,
            cuenta_codigo=CUENTA_RET_ISLR,
            descripcion="Retención ISLR",
            debe=Decimal('0.00'),
            haber=Decimal(factura.ret_islr)
        )

    if getattr(factura, 'ret_municipal', 0) and Decimal(factura.ret_municipal) > 0:
        MovimientoRepository.crear_movimiento(
            asiento=asiento,
            cuenta_codigo=CUENTA_RET_MUNIC,
            descripcion="Retención municipal",
            debe=Decimal('0.00'),
            haber=Decimal(factura.ret_municipal)
        )

    # Haber: proveedor (cuenta por pagar - total)
    MovimientoRepository.crear_movimiento(
        asiento=asiento,
        cuenta_codigo=CUENTA_POR_PAGAR,
        descripcion="Cuenta por pagar a proveedor",
        debe=Decimal('0.00'),
        haber=Decimal(getattr(factura, 'total_factura', factura.monto_base))
    )

    return asiento
