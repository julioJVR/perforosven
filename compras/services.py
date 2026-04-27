# compras/services.py
from decimal import Decimal
from .repositories import FacturaRepository, ContabilidadRepository
from django.utils import timezone
from django.db import transaction


class FacturaService:
    """
    Servicio que centraliza la creación/validación de facturas y la generación del asiento contable.
    """

    def __init__(self, creado_por=None):
        self.creado_por = creado_por

    @transaction.atomic
    def crear_factura_y_asiento(self, factura_obj):
        """
        factura_obj: instancia de Factura (sin guardar) con los campos necesarios ya llenos.
        """
        # 1) Guardar la factura (repositorio se encarga del .save())
        factura = FacturaRepository.crear(factura_obj)

        # 2) Preparar asiento contable
        # Esto es ejemplo de reglas contables básicas — ajústalas a tus cuentas reales.
        fecha = factura.fecha_factura or timezone.now().date()
        descripcion = f"Registro factura {factura.numero_factura} proveedor {factura.proveedor.nombre_empresa}"
        referencia = factura.numero_factura

        base = factura.calcular_base_en_bs()
        iva = factura.iva
        total = factura.total_factura
        ret_iva = factura.ret_iva
        ret_islr = factura.ret_islr
        ret_mun = factura.ret_municipal

        # REGLAS (ejemplo):
        # - Debe: 520-01 Compras (monto_base)
        # - Debe: 240-01 IVA por pagar (iva)
        # - Haber: 101-01 Banco/Caja (total neto a pagar al proveedor)
        # - Haber: 241-01 Retención IVA (ret_iva)
        # - Haber: 242-01 Retención ISLR (ret_islr)
        # - Haber: 243-01 Retención Municipal (ret_mun)
        #
        # Ajusta los códigos de cuenta a los que hayas creado en contabilidad.CuentaContable

        lineas = []

        # 1) Compra (debe)
        lineas.append({'cuenta_codigo': '520-01', 'debe': base, 'haber': Decimal('0.00'), 'descripcion': 'Monto base compra'})

        # 2) IVA (si aplica) - dependiendo si lo registras como impuesto a cargo o por pagar
        if iva and iva > Decimal('0.00'):
            lineas.append({'cuenta_codigo': '240-01', 'debe': iva, 'haber': Decimal('0.00'), 'descripcion': 'IVA (alícuota)'})

        # 3) Banco/Caja (haber) -> pago al proveedor: monto base + iva - retenciones
        neto_a_pagar = (base + iva) - (ret_iva + ret_islr + ret_mun)
        if neto_a_pagar < Decimal('0.00'):
            neto_a_pagar = Decimal('0.00')
        lineas.append({'cuenta_codigo': '101-01', 'debe': Decimal('0.00'), 'haber': neto_a_pagar, 'descripcion': 'Pago neto al proveedor'})

        # 4) Retenciones (haberes)
        if ret_iva and ret_iva > Decimal('0.00'):
            lineas.append({'cuenta_codigo': '241-01', 'debe': Decimal('0.00'), 'haber': ret_iva, 'descripcion': 'Retención IVA'})

        if ret_islr and ret_islr > Decimal('0.00'):
            lineas.append({'cuenta_codigo': '242-01', 'debe': Decimal('0.00'), 'haber': ret_islr, 'descripcion': 'Retención ISLR'})

        if ret_mun and ret_mun > Decimal('0.00'):
            lineas.append({'cuenta_codigo': '243-01', 'debe': Decimal('0.00'), 'haber': ret_mun, 'descripcion': 'Retención Municipal'})

        # 3) Crear asiento
        asiento = ContabilidadRepository.crear_asiento(fecha=fecha, descripcion=descripcion, referencia=referencia, lineas=lineas, creado_por=self.creado_por)

        # 4) Marcar factura como asiento_generado
        factura.asiento_generado = True
        factura.save()

        return factura, asiento
