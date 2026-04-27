# compras/api/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import FacturaSerializer, ProveedorSerializer
from compras.models import Factura, Proveedor
from compras.services import FacturaService
from rest_framework.decorators import action


class ProveedorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    lookup_field = 'id'


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.select_related('proveedor').all()
    serializer_class = FacturaSerializer

    def perform_create(self, serializer):
        # si se pasó rif_proveedor, resolver
        rif = self.request.data.get('rif_proveedor')
        proveedor = None
        if rif:
            try:
                proveedor = Proveedor.objects.get(rif__iexact=rif.strip())
            except Proveedor.DoesNotExist:
                raise serializers.ValidationError({"rif_proveedor": "Proveedor no encontrado."})
        factura = serializer.save(proveedor=proveedor if proveedor else serializer.validated_data.get('proveedor'))
        # Generar asiento automáticamente usando el servicio
        service = FacturaService(creado_por=self.request.user.username if self.request.user.is_authenticated else None)
        service.crear_factura_y_asiento(factura)

    @action(detail=True, methods=['post'])
    def generar_asiento(self, request, pk=None):
        factura = self.get_object()
        service = FacturaService(creado_por=request.user.username if request.user.is_authenticated else None)
        factura, asiento = service.crear_factura_y_asiento(factura)
        return Response({"asiento_id": asiento.id}, status=status.HTTP_200_OK)
