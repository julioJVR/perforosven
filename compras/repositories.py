# compras/repositories.py
from decimal import Decimal
from .models import Factura
from contabilidad.models import Asiento, AsientoLinea, CuentaContable
from django.db import transaction


class FacturaRepository:
    @staticmethod
    def crear(factura_instance):
        """
        Guarda la factura (instancia ya preparada).
        """
        factura_instance.save()
        return factura_instance

    @staticmethod
    def obtener(pk):
        return Factura.objects.select_related('proveedor').get(pk=pk)


class ContabilidadRepository:
    """
    Repositorio para crear asientos contables.
    - Recibe líneas (cuenta_codigo, debe, haber).
    """
    @staticmethod
    def get_cuenta_por_codigo(codigo):
        return CuentaContable.objects.get(codigo=codigo)

    @staticmethod
    @transaction.atomic
    def crear_asiento(fecha, descripcion, referencia, lineas, creado_por=None):
        """
        lineas: lista de dicts {'cuenta_codigo': '101-01', 'debe': Decimal(...), 'haber': Decimal(...), 'descripcion': '...'}
        """
        asiento = Asiento.objects.create(fecha=fecha, descripcion=descripcion, referencia=referencia, creado_por=creado_por)
        for l in lineas:
            cuenta = ContabilidadRepository.get_cuenta_por_codigo(l['cuenta_codigo'])
            AsientoLinea.objects.create(
                asiento=asiento,
                cuenta=cuenta,
                descripcion=l.get('descripcion', ''),
                debe=(l.get('debe') or Decimal('0.00')),
                haber=(l.get('haber') or Decimal('0.00')),
            )
        return asiento

from .models import Factura, Proveedor, OrdenCompra

class FacturaRepository:

    @staticmethod
    def crear_factura(**kwargs):
        return Factura.objects.create(**kwargs)

    @staticmethod
    def actualizar_factura(factura, **kwargs):
        for key, value in kwargs.items():
            setattr(factura, key, value)
        factura.save()
        return factura

    @staticmethod
    def obtener_factura(id):
        return Factura.objects.filter(id=id).first()


class ProveedorRepository:

    @staticmethod
    def obtener_por_rif(rif):
        return Proveedor.objects.filter(rif__iexact=rif).first()


class OrdenCompraRepository:

    @staticmethod
    def obtener_por_id(id):
        return OrdenCompra.objects.filter(id=id).first()