from ..models import CuentaContable, AsientoContable, MovimientoContable
from decimal import Decimal
from django.utils import timezone

class ContabilidadService:
    """Business logic to generate basic accounting entries."""

    @staticmethod
    def asiento_por_factura(factura, mapping):
        fecha = timezone.now().date()
        asiento = AsientoContable(fecha=fecha, descripcion=f"Asiento factura {factura.numero_factura}",
                                  referencia=f"FAC-{factura.id}", origen='COMPRAS', origen_id=str(factura.id))
        asiento.save()
        def _cuenta(v):
            if isinstance(v, CuentaContable):
                return v
            return CuentaContable.objects.get(codigo=v)
        gasto = _cuenta(mapping.get('gasto'))
        MovimientoContable.objects.create(asiento=asiento, cuenta=gasto, descripcion='Gasto', debe=Decimal(factura.monto_base), haber=Decimal('0'))
        if getattr(factura,'iva',0):
            iva = _cuenta(mapping.get('iva'))
            MovimientoContable.objects.create(asiento=asiento, cuenta=iva, descripcion='IVA', debe=Decimal(factura.iva), haber=Decimal('0'))
        if getattr(factura,'ret_iva',0):
            riva = _cuenta(mapping.get('ret_iva'))
            MovimientoContable.objects.create(asiento=asiento, cuenta=riva, descripcion='Retención IVA', debe=Decimal('0'), haber=Decimal(factura.ret_iva))
        porp = _cuenta(mapping.get('por_pagar'))
        MovimientoContable.objects.create(asiento=asiento, cuenta=porp, descripcion='Proveedor', debe=Decimal('0'), haber=Decimal(factura.total_factura))
        return asiento
