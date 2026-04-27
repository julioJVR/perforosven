from django.db.models import Sum, Case, When, F, DecimalField
from contabilidad.models import CuentaContable, MovimientoContable, AsientoContable


def calcular_saldos(desde=None, hasta=None):
    filtros = {}
    if desde:
        filtros["asiento__fecha__gte"] = desde
    if hasta:
        filtros["asiento__fecha__lte"] = hasta

    qs = (
        MovimientoContable.objects
        .filter(**filtros)
        .values("cuenta__id", "cuenta__codigo", "cuenta__nombre", "cuenta__naturaleza")
        .annotate(
            suma_debe=Sum("debe"),
            suma_haber=Sum("haber"),
            saldo=Case(
                When(cuenta__naturaleza="DEBE", then=F("suma_debe") - F("suma_haber")),
                When(cuenta__naturaleza="HABER", then=F("suma_haber") - F("suma_debe")),
                output_field=DecimalField(max_digits=18, decimal_places=2)
            )
        )
        .order_by("cuenta__codigo")
    )

    return list(qs)
