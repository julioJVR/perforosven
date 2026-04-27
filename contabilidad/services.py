# contabilidad/services.py
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
import logging

from .models import CuentaContable, AsientoContable, MovimientoContable

logger = logging.getLogger(__name__)

def _get_cuenta_by_codigo(codigo):
    """
    Intentamos buscar la cuenta contable por código.
    Si no existe, lanzamos excepción para que el integrador la cree antes.
    """
    try:
        return CuentaContable.objects.get(codigo=codigo)
    except CuentaContable.DoesNotExist:
        raise ValueError(f"Cuenta contable con código '{codigo}' no encontrada. Por favor crea la cuenta antes.")

@transaction.atomic
def generar_asiento_desde_factura(factura):
    """
    Genera un asiento contable simple para la factura de proveedor.
    - Crea AsientoContable
    - Crea LineaAsiento para cada movimiento (gasto, iva crédito fiscal, retenciones, proveedor)
    Reglas de cuentas (temporal): puedes parametrizar estas cuentas en la BD.
    """
    # calculamos total a pagar (total factura menos retenciones)
    total_factura = factura.total_factura or Decimal('0.00')
    retenciones = (factura.ret_iva or Decimal('0.00')) + (factura.ret_islr or Decimal('0.00')) + (factura.ret_municipal or Decimal('0.00'))
    total_pagar = (total_factura - retenciones).quantize(Decimal('0.01'))

    descripcion = f"Asiento por factura Nº {factura.numero_factura} / Proveedor: {factura.proveedor.nombre_empresa if factura.proveedor else 'N/D'}"
    referencia = f"FAC-{factura.id or '0'}"

    # Cuentas (códigos temporales — modificar por configuración/DB si lo deseas)
    CUENTA_GASTO = "5-01-01"
    CUENTA_IVA_CRED_FISCAL = "1-03-05"
    CUENTA_RET_IVA = "2-02-01"
    CUENTA_RET_ISLR = "2-02-02"
    CUENTA_RET_MUNIC = "2-02-03"
    CUENTA_POR_PAGAR = "2-01-01"

    # Validaciones de existencia de cuentas
    cuentas_a_validar = [CUENTA_GASTO, CUENTA_IVA_CRED_FISCAL, CUENTA_RET_IVA, CUENTA_RET_ISLR, CUENTA_RET_MUNIC, CUENTA_POR_PAGAR]
    cuentas_obj = {}
    for c in cuentas_a_validar:
        cuentas_obj[c] = _get_cuenta_by_codigo(c)

    # crear asiento
    asiento = AsientoContable.objects.create(
        fecha=timezone.now().date(),
        descripcion=descripcion,
        referencia=referencia
    )

    # --- Debe: gasto (monto base) ---
    monto_base = (factura.monto_base or Decimal('0.00'))
    if monto_base > 0:
        MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuentas_obj[CUENTA_GASTO],
            descripcion="Gasto/Servicio adquirido",
            debe=monto_base,
            haber=Decimal('0.00')
        )

    # --- Debe: IVA (crédito fiscal) si aplica ---
    iva = (factura.iva or Decimal('0.00'))
    if iva > 0:
        MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuentas_obj[CUENTA_IVA_CRED_FISCAL],
            descripcion="Crédito fiscal IVA",
            debe=iva,
            haber=Decimal('0.00')
        )

    # --- Haber: retenciones ---
    ret_iva = (factura.ret_iva or Decimal('0.00'))
    if ret_iva > 0:
        MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuentas_obj[CUENTA_RET_IVA],
            descripcion="Retención IVA",
            debe=Decimal('0.00'),
            haber=ret_iva
        )

    ret_islr = (factura.ret_islr or Decimal('0.00'))
    if ret_islr > 0:
        MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuentas_obj[CUENTA_RET_ISLR],
            descripcion="Retención ISLR",
            debe=Decimal('0.00'),
            haber=ret_islr
        )

    ret_mun = (factura.ret_municipal or Decimal('0.00'))
    if ret_mun > 0:
        MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuentas_obj[CUENTA_RET_MUNIC],
            descripcion="Retención municipal",
            debe=Decimal('0.00'),
            haber=ret_mun
        )

    # --- Haber: proveedor / cuenta por pagar ---
    if total_pagar != Decimal('0.00'):
        MovimientoContable.objects.create(
            asiento=asiento,
            cuenta=cuentas_obj[CUENTA_POR_PAGAR],
            descripcion=f"Cuenta por pagar a proveedor ({factura.proveedor.nombre_empresa if factura.proveedor else ''})",
            debe=Decimal('0.00'),
            haber=total_pagar
        )

    # Verificamos que esté cuadrado
    suma_debe = sum([l.debe for l in asiento.lineas.all()])
    suma_haber = sum([l.haber for l in asiento.lineas.all()])

    if suma_debe.quantize(Decimal('0.01')) != suma_haber.quantize(Decimal('0.01')):
        # Opcional: podrías querer eliminar asiento y lanzar error
        logger.error("Asiento generado NO está cuadrado (Debe: %s, Haber: %s). Factura: %s", suma_debe, suma_haber, factura.id)
        raise ValueError(f"Asiento no cuadrado (Debe={suma_debe}, Haber={suma_haber}). Revisa configuración de cuentas.")

    return asiento
