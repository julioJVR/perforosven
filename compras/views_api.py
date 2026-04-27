# compras/views_api.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Factura
from .serializers import FacturaSerializer
from django.shortcuts import get_object_or_404

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.select_related('proveedor').all().order_by('-fecha_factura')
    serializer_class = FacturaSerializer

    def perform_create(self, serializer):
        factura = serializer.save()
        # Generar asiento automático si existe el servicio
        try:
            from contabilidad.services.asiento_service import generar_asiento_compra
            generar_asiento_compra(factura)
        except Exception as e:
            # no detener la creación; solo informar
            # puedes registrar este error en logs
            print("Error generando asiento:", e)
