from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('compras/', include(('compras.urls', 'compras'), namespace='compras')),
    path("contabilidad/", include("contabilidad.urls")),
    #path('ventas/', include('ventas.urls')),
    path('ventas/', include(('ventas.urls', 'ventas'), namespace='ventas')),
    path('api/compras/', include(('compras.urls_api', 'compras_api'), namespace='compras_api')),
    path('api/contabilidad/', include(('contabilidad.urls', 'contabilidad_api'), namespace='contabilidad_api')),
    
]

