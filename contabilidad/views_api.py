from rest_framework import viewsets
from .models import CuentaContable, AsientoContable
from .serializers import CuentaContableSerializer, AsientoContableSerializer

class CuentaContableViewSet(viewsets.ModelViewSet):
    queryset = CuentaContable.objects.all().order_by('codigo')
    serializer_class = CuentaContableSerializer

class AsientoContableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AsientoContable.objects.all().order_by('-fecha')
    serializer_class = AsientoContableSerializer
