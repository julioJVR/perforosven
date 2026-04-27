# contabilidad/urls.py
from django.urls import path
from . import views

app_name = "contabilidad"

urlpatterns = [
    path("dashboard/", views.dashboard_contabilidad, name="dashboard_contabilidad"),

    # Cuentas
    path("cuentas/", views.cuentas_list, name="cuentas_list"),
    path("cuentas/nuevo/", views.cuentas_create, name="cuentas_create"),
    path("cuentas/editar/<int:pk>/", views.cuentas_edit, name="cuentas_edit"),
    path("cuentas/eliminar/<int:pk>/", views.cuentas_delete, name="cuentas_delete"),

    # Asientos
    path("asientos/", views.asientos_list, name="asientos_list"),
    path("asientos/nuevo/", views.asientos_create, name="asientos_create"),
    path("asientos/<int:pk>/", views.asientos_detail, name="asientos_detail"),
    path("asientos/eliminar/<int:pk>/", views.asientos_delete, name="asientos_delete"),

    # Importar plan
    path("importar-plan/", views.importar_plan_view, name="importar_plan"),

    # Reportes submenu (opcional)
    path("reportes/", views.menu_reportes, name="menu_reportes"),
    path("reportes/balance/", views.balance_general, name="balance_general"),
    path("reportes/estado-resultados/", views.estado_resultados, name="estado_resultados"),
    path("reportes/pl-analitico/", views.pl_analitico, name="pl_analitico"),
    path("reportes/flujo-efectivo/", views.flujo_efectivo, name="flujo_efectivo"),
]
