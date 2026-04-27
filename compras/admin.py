# compras/admin.py

from django.contrib import admin
from .models import Factura  # ahora compras solo maneja Factura

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "proveedor",
        "numero_factura",
        "fecha_factura",
        "moneda",
        "total_factura",
    )
    search_fields = ("numero_factura", "proveedor__nombre_empresa")
    list_filter = ("moneda", "fecha_factura")
