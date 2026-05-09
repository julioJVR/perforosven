# compras/services/facturas.py

from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from ..repositories import (
    FacturaRepository,
    ContabilidadRepository,
)


class FacturaService:
    """
    Servicio encargado de:

    - Registrar facturas
    - Validar reglas de negocio
    - Generar asiento contable automático
    """

    def __init__(self, creado_por=None):
        self.creado_por = creado_por

    @transaction.atomic
    def crear_factura_y_asiento(self, factura_obj):
        """
        Guarda una factura y genera automáticamente
        su asiento contable asociado.
        """

        # =========================
        # 1. Guardar factura
        # =========================
        factura = FacturaRepository.crear(factura_obj)

        # =========================
        # 2. Preparar datos contables
        # =========================
        fecha = factura.fecha_factura or timezone.now().date()

        descripcion = (
            f"Registro factura "
            f"{factura.numero_factura} - "
            f"{factura.proveedor.nombre_empresa}"
        )

        referencia = factura.numero_factura

        # =========================
        # 3. Calcular base imponible
        # =========================
        base = (
            factura.monto_base * factura.tasa_cambio
            if factura.moneda == 'USD'
            else factura.monto_base
        )

        iva = factura.iva or Decimal('0.00')
        ret_iva = factura.ret_iva or Decimal('0.00')
        ret_islr = factura.ret_islr or Decimal('0.00')
        ret_mun = factura.ret_municipal or Decimal('0.00')

        # =========================
        # 4. Construir líneas contables
        # =========================
        lineas = self._generar_lineas_contables(
            base=base,
            iva=iva,
            ret_iva=ret_iva,
            ret_islr=ret_islr,
            ret_mun=ret_mun,
        )

        # =========================
        # 5. Crear asiento
        # =========================
        asiento = ContabilidadRepository.crear_asiento(
            fecha=fecha,
            descripcion=descripcion,
            referencia=referencia,
            lineas=lineas,
            creado_por=self.creado_por,
        )

        return factura, asiento

    def _generar_lineas_contables(
        self,
        base,
        iva,
        ret_iva,
        ret_islr,
        ret_mun,
    ):
        """
        Genera las líneas del asiento contable.
        """

        lineas = []

        # =========================
        # Gasto / Compra
        # =========================
        lineas.append({
            'cuenta_codigo': '520-01',
            'debe': base,
            'haber': Decimal('0.00'),
            'descripcion': 'Monto base compra',
        })

        # =========================
        # IVA Crédito Fiscal
        # =========================
        if iva > Decimal('0.00'):
            lineas.append({
                'cuenta_codigo': '240-01',
                'debe': iva,
                'haber': Decimal('0.00'),
                'descripcion': 'IVA crédito fiscal',
            })

        # =========================
        # Neto a pagar
        # =========================
        neto_a_pagar = (
            (base + iva)
            - (ret_iva + ret_islr + ret_mun)
        )

        if neto_a_pagar < Decimal('0.00'):
            neto_a_pagar = Decimal('0.00')

        lineas.append({
            'cuenta_codigo': '101-01',
            'debe': Decimal('0.00'),
            'haber': neto_a_pagar,
            'descripcion': 'Cuenta por pagar proveedor',
        })

        # =========================
        # Retención IVA
        # =========================
        if ret_iva > Decimal('0.00'):
            lineas.append({
                'cuenta_codigo': '241-01',
                'debe': Decimal('0.00'),
                'haber': ret_iva,
                'descripcion': 'Retención IVA',
            })

        # =========================
        # Retención ISLR
        # =========================
        if ret_islr > Decimal('0.00'):
            lineas.append({
                'cuenta_codigo': '242-01',
                'debe': Decimal('0.00'),
                'haber': ret_islr,
                'descripcion': 'Retención ISLR',
            })

        # =========================
        # Retención Municipal
        # =========================
        if ret_mun > Decimal('0.00'):
            lineas.append({
                'cuenta_codigo': '243-01',
                'debe': Decimal('0.00'),
                'haber': ret_mun,
                'descripcion': 'Retención Municipal',
            })

        return lineas