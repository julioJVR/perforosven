from django.urls import path

from compras.views import views
from compras.views import views_facturas

app_name = 'compras'

urlpatterns = [

    # =========================
    # DASHBOARD
    # =========================
    path('', views.dashboard_compras, name='dashboard_compras'),

    # =========================
    # PROVEEDORES
    # =========================
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/nuevo/', views.nuevo_proveedor, name='nuevo_proveedor'),
    path('proveedores/editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    # =========================
    # PRODUCTOS
    # =========================
    path('productos/', views.lista_productos, name='producto_list'),
    path('productos/', views.lista_productos, name='lista_productos'),

    path('productos/nuevo/', views.nuevo_producto, name='producto_create'),
    path('productos/nuevo/', views.nuevo_producto, name='nuevo_producto'),

    path('productos/editar/<int:pk>/', views.editar_producto, name='producto_update'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),

    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='producto_delete'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # =========================
    # ORDENES
    # =========================
    path('ordenes/', views.lista_ordenes, name='orden_list'),
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),

    path('ordenes/nueva/', views.nueva_orden, name='orden_create'),
    path('ordenes/nueva/', views.nueva_orden, name='nueva_orden'),

    path('ordenes/editar/<int:pk>/', views.editar_orden, name='orden_update'),
    path('ordenes/editar/<int:pk>/', views.editar_orden, name='editar_orden'),

    path('ordenes/eliminar/<int:pk>/', views.eliminar_orden, name='orden_delete'),
    path('ordenes/eliminar/<int:pk>/', views.eliminar_orden, name='eliminar_orden'),

    path('ordenes/ver/<int:pk>/', views.ver_orden, name='ver_orden'),
    path('ordenes/pdf/<int:pk>/', views.imprimir_orden_pdf, name='imprimir_orden_pdf'),
    path('ordenes/excel/<int:pk>/', views.exportar_orden_excel, name='exportar_orden_excel'),

    # =========================
    # FACTURAS
    # =========================
    path('facturas/', views_facturas.lista_facturas, name='lista_facturas'),
    path('facturas/nuevo/', views_facturas.crear_factura, name='crear_factura'),
    path('facturas/editar/<int:pk>/', views_facturas.editar_factura, name='editar_factura'),
    path('facturas/eliminar/<int:pk>/', views_facturas.eliminar_factura, name='eliminar_factura'),

    path('buscar-proveedor/', views_facturas.buscar_proveedor, name='buscar_proveedor'),

    path(
        'facturas-pendientes/',
        views.facturas_pendientes,
        name='facturas_pendientes'
    ),
]