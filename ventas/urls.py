from django.urls import path
from ventas.views.dashboard import dashboard

from ventas.views.clientes import (
    clientes_list,
    cliente_create,
    cliente_edit
)

from ventas.views.contratos import (
    contratos_list,
    contrato_create,
    contrato_edit,
    contrato_delete,
    obtener_partidas_contrato
)

from ventas.views.cotizaciones import (
    cotizaciones_list,
    cotizacion_create,
    cotizacion_edit,
    partidas_por_contrato
)

app_name = 'ventas'

urlpatterns = [
    path('', dashboard, name='dashboard'),

    # CLIENTES
    path('clientes/', clientes_list, name='clientes'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_edit, name='cliente_edit'),

    # CONTRATOS
    path('contratos/', contratos_list, name='contratos'),
    path('contratos/nuevo/', contrato_create, name='contrato_create'),
    path('contratos/<int:pk>/editar/', contrato_edit, name='contrato_edit'),
    path('contratos/<int:pk>/eliminar/', contrato_delete, name='contrato_delete'),

    # API CONTRATOS
    path('contratos/<int:pk>/partidas/', obtener_partidas_contrato, name='obtener_partidas_contrato'),

    # COTIZACIONES
    path('cotizaciones/', cotizaciones_list, name='cotizaciones'),
    path('cotizaciones/nueva/', cotizacion_create, name='cotizacion_create'),
    path('cotizaciones/<int:pk>/editar/', cotizacion_edit, name='cotizacion_edit'),

    # API COTIZACIONES
    path('cotizaciones/contrato/<int:contrato_id>/partidas/', partidas_por_contrato, name='partidas_por_contrato'),
]