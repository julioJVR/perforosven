from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación
    path('accounts/', include('accounts.urls')),

    # Dashboard principal / Core
    path('', include(('core.urls', 'core'), namespace='core')),

    # Módulos principales
    path('compras/', include(('compras.urls', 'compras'), namespace='compras')),
    path('ventas/', include(('ventas.urls', 'ventas'), namespace='ventas')),
    path('contabilidad/', include(('contabilidad.urls', 'contabilidad'), namespace='contabilidad')),
    path('configuracion/', include(('configuracion.urls', 'configuracion'), namespace='configuracion')),

    # APIs internas
    path('api/compras/', include(('compras.urls_api', 'compras_api'), namespace='compras_api')),
    path('api/contabilidad/', include(('contabilidad.urls', 'contabilidad_api'), namespace='contabilidad_api')),
]

# Debug Toolbar solo en desarrollo
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns