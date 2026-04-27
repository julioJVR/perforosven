# contabilidad/admin.py
from django.contrib import admin
from .models import CuentaContable, AsientoContable, MovimientoContable


@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "tipo", "nivel", "es_activo")
    list_filter = ("tipo", "nivel", "es_activo")
    search_fields = ("codigo", "nombre")


@admin.register(AsientoContable)
class AsientoContableAdmin(admin.ModelAdmin):
    list_display = ("numero", "fecha", "descripcion", "total_debe", "total_haber")
    search_fields = ("numero", "descripcion")
    date_hierarchy = "fecha"


@admin.register(MovimientoContable)
class MovimientoContableAdmin(admin.ModelAdmin):
    list_display = ("asiento", "cuenta", "descripcion", "debe", "haber")
    search_fields = ("descripcion",)
    list_filter = ("cuenta",)

