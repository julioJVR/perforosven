from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    """
    Dashboard general de SIAC Perforosven.
    Muestra los accesos a los distintos módulos del sistema.
    """
    modulos = [
        {
            "nombre": "Compras",
            "descripcion": "Gestión de proveedores, órdenes de compra, facturas.",
            "icono": "bi-cart-fill",
            "url": "compras:dashboard_compras",
            "color": "bg-blue-700 hover:bg-blue-800"
        },
        {
            "nombre": "Ventas",
            "descripcion": "Control de clientes, contratos, proformas y facturación.",
            "icono": "bi-cash-coin",
            "url": "ventas:dashboard",
            "color": "bg-blue-700 hover:bg-green-800"
        },
        {
            "nombre": "Tesorería",
            "descripcion": "Pagos, bancos y conciliaciones.",
            "icono": "bi-bank2",
            "url": "#",
            "color": "bg-yellow-600 hover:bg-yellow-700"
        },
        {
            "nombre": "Contabilidad",
            "descripcion": "Registros contables, balances y reportes financieros.",
            "icono": "bi-clipboard-data",
            "url": "contabilidad:dashboard_contabilidad",
            "color": "bg-blue-700 hover:bg-blue-800"
        },
        {
            "nombre": "Tributos",
            "descripcion": "Cálculo de impuestos, declaraciones y reportes fiscales.",
            "icono": "bi-receipt",
            "url": "#",
            "color": "bg-red-700 hover:bg-red-800"
        },
        {
            "nombre": "Presupuesto",
            "descripcion": "Control Presupuestario, Control de Gastos, Presupuesto y Proyecciones.",
            "icono": "bi-calculator-fill",
            "url": "#",
            "color": "bg-red-700 hover:bg-red-800"
        },
        {
            "nombre": "Recursos Humanos",
            "descripcion": "Nómina, vacaciones, utilidades y reportes laborales.",
            "icono": "bi-people-fill",
            "url": "#",
            "color": "bg-red-700 hover:bg-red-800"
        },
        {
            "nombre": "Almacen",
            "descripcion": "Requisiciones, materiales, entradas, salidas, reportes.",
            "icono": "bi bi-shop-window",
            "url": "#",
            "color": "bg-red-700 hover:bg-red-800"
        },
        {
            "nombre": "Configuracion",
            "descripcion": "Usuarios, creacion, seguridad.",
            "icono": "bi bi-gear",
            "url": "#",
            "color": "bg-red-700 hover:bg-red-800"
        }
    ]
    return render(request, 'core/inicio.html', {'modulos': modulos})
