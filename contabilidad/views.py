# contabilidad/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, F
from django.http import HttpResponse
from matplotlib.style import context
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from .forms import CuentaContableForm, AsientoContableForm, MovimientoContableForm
from .models import CuentaContable, AsientoContable, MovimientoContable
from django.contrib.auth.decorators import login_required

# ---------------- DASHBOARD ----------------
def dashboard_contabilidad(request):
    total_cuentas = CuentaContable.objects.count()
    total_asientos = AsientoContable.objects.count()
    activos = CuentaContable.objects.filter(codigo__startswith="1").count()
    pasivos = CuentaContable.objects.filter(codigo__startswith="2").count()

    # asientos no cuadrados
    asientos = AsientoContable.objects.all().order_by("-fecha")
    asientos_no_cuadrados = []
    for a in asientos:
        a.actualizar_totales()  # asegura totales
        if not a.esta_cuadrado():
            asientos_no_cuadrados.append(a)

    context = {
        "total_cuentas": total_cuentas,
        "total_asientos": total_asientos,
        "activos": activos,
        "pasivos": pasivos,
        "asientos_no_cuadrados": asientos_no_cuadrados,
    }
    return render(request, "contabilidad/dashboard.html", context)


# ---------------- CUENTAS CRUD ----------------
def cuentas_list(request):
    cuentas = CuentaContable.objects.order_by("codigo").all()
    return render(request, "contabilidad/cuentas/list.html", {"cuentas": cuentas})


def cuentas_create(request):
    form = CuentaContableForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Cuenta creada correctamente.")
        return redirect("contabilidad:cuentas_list")
    return render(request, "contabilidad/cuentas/cuentas_create.html", {"form": form, "accion": "Nueva Cuenta"})


def cuentas_edit(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    form = CuentaContableForm(request.POST or None, instance=cuenta)
    if form.is_valid():
        form.save()
        messages.success(request, "Cuenta actualizada.")
        return redirect("contabilidad:cuentas_list")
    return render(request, "contabilidad/cuentas/form.html", {"form": form, "accion": "Editar Cuenta"})


def cuentas_delete(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    if request.method == "POST":
        cuenta.delete()
        messages.success(request, "Cuenta eliminada.")
        return redirect("contabilidad:cuentas_list")
    return render(request, "contabilidad/cuentas/confirm_delete.html", {"objeto": cuenta})


# ---------------- ASIENTOS CRUD ----------------
def asientos_list(request):
    asientos = AsientoContable.objects.all().order_by("-fecha")
    #return render(request, "contabilidad/asientos_list.html", {"asientos": asientos})
    return render(request, "contabilidad/asientos/list.html", {"asientos": asientos})


def asientos_create(request):
    form = AsientoContableForm(request.POST or None)
    MovimientoForm = MovimientoContableForm
    cuentas = CuentaContable.objects.order_by("codigo").all()

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            asiento = form.save()
            # esperar listas desde el form dinamico
            cuentas_ids = request.POST.getlist("cuenta_id[]")
            descs = request.POST.getlist("descripcion_linea[]")
            debes = request.POST.getlist("debe[]")
            habers = request.POST.getlist("haber[]")

            for i, cid in enumerate(cuentas_ids):
                if not cid:
                    continue
                MovimientoContable.objects.create(
                    asiento=asiento,
                    cuenta_id=int(cid),
                    descripcion=descs[i] if i < len(descs) else "",
                    debe=debes[i] or 0,
                    haber=habers[i] or 0,
                )
            asiento.actualizar_totales()

        messages.success(request, "Asiento registrado.")
        return redirect("contabilidad:asientos_list")

    return render(request, "contabilidad/asientos/form.html", {"form": form, "cuentas": cuentas})


def asientos_detail(request, pk):
    asiento = get_object_or_404(AsientoContable, pk=pk)
    lineas = asiento.lineas.select_related("cuenta").all()
    return render(request, "contabilidad/asientos/detail.html", {"asiento": asiento, "lineas": lineas})


def asientos_delete(request, pk):
    asiento = get_object_or_404(AsientoContable, pk=pk)
    if request.method == "POST":
        asiento.delete()
        messages.success(request, "Asiento eliminado.")
        return redirect("contabilidad:asientos_list")
    return render(request, "contabilidad/confirm_delete.html", {"objeto": asiento})


# ---------------- IMPORTAR PLAN ----------------
def importar_plan_view(request):
    """Sube un Excel con columnas: codigo, nombre, tipo, naturaleza, nivel, padre_codigo (opcional)."""
    if request.method == "POST":
        file = request.FILES.get("archivo")
        if not file:
            messages.error(request, "Seleccione un archivo.")
            return redirect("contabilidad:importar_plan")

        if not file.name.lower().endswith((".xlsx", ".xls")):
            messages.error(request, "Formato inválido. Use .xlsx o .xls")
            return redirect("contabilidad:importar_plan")

        try:
            # prefer pandas if disponible
            try:
                df = pd.read_excel(file)
            except Exception:
                wb = load_workbook(file)
                ws = wb.active
                data = list(ws.values)
                headers = [str(h).strip().lower() for h in data[0]]
                rows = [dict(zip(headers, r)) for r in data[1:]]
                df = pd.DataFrame(rows)

            required = {"codigo", "nombre", "tipo"}
            df_cols = set(c.lower() for c in df.columns)
            if not required.issubset(df_cols):
                messages.error(request, f"Columnas requeridas: {', '.join(required)}")
                return redirect("contabilidad:importar_plan")

            registros = 0
            with transaction.atomic():
                for _, row in df.iterrows():
                    codigo = str(row.get("codigo")).strip()
                    nombre = str(row.get("nombre")).strip()
                    tipo = str(row.get("tipo")).strip().upper()
                    if not codigo or not nombre or not tipo:
                        continue
                    if CuentaContable.objects.filter(codigo=codigo).exists():
                        continue
                    # padre opcional por codigo
                    padre_codigo = row.get("padre_codigo") or row.get("padre") or None
                    padre = None
                    if padre_codigo:
                        padre = CuentaContable.objects.filter(codigo=str(padre_codigo).strip()).first()
                    CuentaContable.objects.create(
                        codigo=codigo,
                        nombre=nombre,
                        tipo=tipo,
                        naturaleza=row.get("naturaleza") or "D",
                        nivel=int(row.get("nivel") or 1),
                        padre=padre,
                    )
                    registros += 1

            messages.success(request, f"Importación correcta: {registros} cuentas creadas.")
            return redirect("contabilidad:cuentas_list")

        except Exception as e:
            messages.error(request, f"Error importando: {e}")
            return redirect("contabilidad:importar_plan")

    return render(request, "contabilidad/importar_plan.html")


# ---------------- REPORTES (BÁSICOS) ----------------
def menu_reportes(request):
    return render(request, "contabilidad/reports/menu_reportes.html")


def balance_general(request):
    # sumar saldos por prefijos 1/2/3 usando movimientos
    total_activo = MovimientoContable.objects.filter(cuenta__codigo__startswith="1").aggregate(
        saldo=Sum(F("debe") - F("haber"))
    )["saldo"] or 0
    total_pasivo = MovimientoContable.objects.filter(cuenta__codigo__startswith="2").aggregate(
        saldo=Sum(F("haber") - F("debe"))
    )["saldo"] or 0
    total_patrimonio = MovimientoContable.objects.filter(cuenta__codigo__startswith="3").aggregate(
        saldo=Sum(F("haber") - F("debe"))
    )["saldo"] or 0

    context = {
        "total_activo": total_activo,
        "total_pasivo": total_pasivo,
        "total_patrimonio": total_patrimonio,
    }
    return render(request, "contabilidad/reports/balance_general.html", context)


def estado_resultados(request):

    # LISTA DE INGRESOS (cuentas 4)
    ingresos = MovimientoContable.objects.filter(
        cuenta__codigo__startswith="4"
    ).values(
        codigo=F("cuenta__codigo"),
        nombre=F("cuenta__nombre")
    ).annotate(
        saldo=Sum(F("haber") - F("debe"))
    )

    # LISTA DE GASTOS (cuentas 6)
    gastos = MovimientoContable.objects.filter(
        cuenta__codigo__startswith="6"
    ).values(
        codigo=F("cuenta__codigo"),
        nombre=F("cuenta__nombre")
    ).annotate(
        saldo=Sum(F("debe") - F("haber"))
    )

    # TOTALES
    total_ingresos = sum(item["saldo"] for item in ingresos)
    total_gastos = sum(item["saldo"] for item in gastos)

    utilidad = total_ingresos - total_gastos

    context = {
        "ingresos": ingresos,
        "gastos": gastos,
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "utilidad": utilidad,
        "chart_labels": ["Ene", "Feb", "Mar"],
        "chart_values": [100, 200, 150],
    }

    return render(request, "contabilidad/reports/estado_resultados.html", context)

def pl_analitico(request):
    # placeholder simple: meses estáticos, en tu instalación puedes generar dinámico por período
    labels = ["Ene", "Feb", "Mar", "Abr", "May"]
    valores_ingresos = [10000, 12000, 11000, 14000, 16000]
    valores_gastos = [4000, 4500, 4200, 4800, 5000]
    return render(request, "contabilidad/reports/pl_analitico.html", {
        "labels": labels,
        "valores_ingresos": valores_ingresos,
        "valores_gastos": valores_gastos,
    })


def flujo_efectivo(request):

    # ACTIVIDADES DE OPERACIÓN
    operacion = MovimientoContable.objects.filter(
        cuenta__codigo__startswith="7"
    ).values(
        codigo=F("cuenta__codigo"),
        nombre=F("cuenta__nombre")
    ).annotate(
        saldo=Sum(F("haber") - F("debe"))
    )

    total_operacion = sum(x["saldo"] for x in operacion)

    # ACTIVIDADES DE INVERSIÓN
    inversion = MovimientoContable.objects.filter(
        cuenta__codigo__startswith="8"
    ).values(
        codigo=F("cuenta__codigo"),
        nombre=F("cuenta__nombre")
    ).annotate(
        saldo=Sum(F("haber") - F("debe"))
    )

    total_inversion = sum(x["saldo"] for x in inversion)

    # ACTIVIDADES DE FINANCIAMIENTO
    financiacion = MovimientoContable.objects.filter(
        cuenta__codigo__startswith="9"
    ).values(
        codigo=F("cuenta__codigo"),
        nombre=F("cuenta__nombre")
    ).annotate(
        saldo=Sum(F("haber") - F("debe"))
    )

    total_financiacion = sum(x["saldo"] for x in financiacion)

    # RESULTADO FINAL
    variacion_efectivo = total_operacion + total_inversion + total_financiacion

    context = {
        "operacion": operacion,
        "inversion": inversion,
        "financiacion": financiacion,
        "total_operacion": total_operacion,
        "total_inversion": total_inversion,
        "total_financiacion": total_financiacion,
        "variacion_efectivo": variacion_efectivo,
    }

    return render(request, "contabilidad/reports/flujo_efectivo.html", context)
