from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def inicio(request):
    """
    Dashboard general de SIAC Perforosven.
    Muestra módulos según el rol del usuario autenticado.
    """

    todos_modulos = [
        {
            "nombre": "Compras",
            "descripcion": "Gestión de proveedores, órdenes de compra, facturas.",
            "icono": "bi-cart-fill",
            "url": "compras:dashboard_compras",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin", "compras"]
        },
        {
            "nombre": "Ventas",
            "descripcion": "Control de clientes, contratos, proformas y facturación.",
            "icono": "bi-cash-coin",
            "url": "ventas:dashboard",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin", "ventas"]
        },
        {
            "nombre": "Tesorería",
            "descripcion": "Pagos, bancos y conciliaciones.",
            "icono": "bi-bank2",
            "url": "#",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin"]
        },
        {
            "nombre": "Contabilidad",
            "descripcion": "Registros contables, balances y reportes financieros.",
            "icono": "bi-clipboard-data",
            "url": "contabilidad:dashboard_contabilidad",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin", "contabilidad"]
        },
        {
            "nombre": "Tributos",
            "descripcion": "Cálculo de impuestos, declaraciones y reportes fiscales.",
            "icono": "bi-receipt",
            "url": "#",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin"]
        },
        {
            "nombre": "Presupuesto",
            "descripcion": "Control presupuestario, gastos y proyecciones.",
            "icono": "bi-calculator-fill",
            "url": "#",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin"]
        },
        {
            "nombre": "Recursos Humanos",
            "descripcion": "Nómina, vacaciones, utilidades y reportes laborales.",
            "icono": "bi-people-fill",
            "url": "#",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin"]
        },
        {
            "nombre": "Almacen",
            "descripcion": "Requisiciones, materiales, entradas y salidas.",
            "icono": "bi-shop-window",
            "url": "#",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin"]
        },
        {
            "nombre": "Configuracion",
            "descripcion": "Usuarios, roles y seguridad.",
            "icono": "bi-gear-fill",
            "url": "core:lista_usuarios",
            "color": "bg-blue-700 hover:bg-blue-800",
            "roles": ["superadmin", "admin"]
        }
    ]

    rol_usuario = getattr(request.user, "role", None)

    modulos = [
        modulo for modulo in todos_modulos
        if rol_usuario in modulo["roles"]
    ]

    return render(request, 'core/inicio.html', {
        'modulos': modulos
    })