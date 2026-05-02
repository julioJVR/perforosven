from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # <-- Importar settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # ← NUEVA
    path('', include(('core.urls', 'core'), namespace='core')),
    path('compras/', include(('compras.urls', 'compras'), namespace='compras')),
    path("contabilidad/", include("contabilidad.urls")),
    path('ventas/', include(('ventas.urls', 'ventas'), namespace='ventas')),
    #path('configuracion/', include(('configuracion.urls', 'configuracion'), namespace='configuracion')),
    path('api/compras/', include(('compras.urls_api', 'compras_api'), namespace='compras_api')),
    path('api/contabilidad/', include(('contabilidad.urls', 'contabilidad_api'), namespace='contabilidad_api')),
    
]

# Solo incluir el debug toolbar si DEBUG está activo
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

