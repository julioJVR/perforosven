# compras/urls_api.py
from rest_framework import routers
from .views_api import FacturaViewSet

router = routers.DefaultRouter()
router.register(r'facturas', FacturaViewSet, basename='factura')

urlpatterns = router.urls
