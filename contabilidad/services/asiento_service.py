from django.db import transaction
from contabilidad.repositories.cuenta_repository import CuentaRepository
from contabilidad.repositories.asientorepository import AsientoRepository


class AsientoService:

    @staticmethod
    @transaction.atomic
    def generar_asiento_compra(factura):
        """
        Genera el asiento contable NIIF por una factura de compras.
        """
        asiento = AsientoRepository.create_asiento(
            descripcion=f"Registro de factura de compra N° {factura.numero}",
            referencia=factura.numero,
            origen="COMPRAS",
            origen_id=factura.id,
            total_debe=factura.total,
            total_haber=factura.total
        )

        # 1. Inventario (DEBE)
        cuenta_inventario = CuentaRepository.get_by_codigo("1101-01")
        AsientoRepository.add_movimiento(
            asiento, cuenta_inventario, debe=factura.base_imponible
        )

        # 2. IVA Crédito Fiscal (DEBE)
        cuenta_iva_cf = CuentaRepository.get_by_codigo("2104-01")
        AsientoRepository.add_movimiento(
            asiento, cuenta_iva_cf, debe=factura.iva
        )

        # 3. Proveedores (HABER)
        cuenta_proveedores = CuentaRepository.get_by_codigo("2102-01")
        AsientoRepository.add_movimiento(
            asiento, cuenta_proveedores, haber=factura.total
        )

        return asiento
