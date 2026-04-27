# compras/views_facturas.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal

from .models import Factura, Proveedor
from .forms import FacturaForm

from django.utils import timezone
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField

def buscar_proveedor(request):
    rif = request.GET.get('rif')
    if not rif:
        return JsonResponse({'error': 'RIF no proporcionado'}, status=400)
    try:
        proveedor = Proveedor.objects.get(rif__iexact=rif.strip())
        return JsonResponse({'id': proveedor.id, 'nombre_empresa': proveedor.nombre_empresa})
    except Proveedor.DoesNotExist:
        return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)

def lista_facturas(request):
    facturas = Factura.objects.select_related('proveedor').all()
    return render(request, 'compras/facturas/list.html', {'facturas': facturas})

def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)

            # Prioridad: RIF escrito por el usuario
            rif = form.cleaned_data.get('rif_proveedor') or ''
            if rif:
                try:
                    proveedor = Proveedor.objects.get(rif__iexact=rif.strip())
                    factura.proveedor = proveedor
                except Proveedor.DoesNotExist:
                    messages.error(request, f"No se encontró un proveedor con el RIF {rif}.")
                    return render(request, 'compras/facturas/form.html', {'form': form, 'accion': 'Crear Factura'})

            # Si no hay proveedor aún, tomar del select
            if not getattr(factura, 'proveedor', None):
                factura.proveedor = form.cleaned_data.get('proveedor')

            # Recalcular en servidor (no confiar en cliente)
            monto_base = form.cleaned_data.get('monto_base') or Decimal('0.00')
            tasa = form.cleaned_data.get('tasa_cambio') or Decimal('1.00')
            moneda = form.cleaned_data.get('moneda')
            aplica_iva = form.cleaned_data.get('aplica_iva')

            base_en_bs = (monto_base * tasa) if moneda == 'USD' else monto_base

            iva = (base_en_bs * Decimal('0.16')) if aplica_iva else Decimal('0.00')
            total = (base_en_bs + iva).quantize(Decimal('0.01'))

            # retenciones porcentuales
            ret_iva_pct = (form.cleaned_data.get('ret_iva_pct') or Decimal('0.00')) / Decimal('100.00')
            ret_islr_pct = (form.cleaned_data.get('ret_islr_pct') or Decimal('0.00')) / Decimal('100.00')
            ret_mun_pct = (form.cleaned_data.get('ret_municipal_pct') or Decimal('0.00')) / Decimal('100.00')

            ret_iva = (base_en_bs * ret_iva_pct).quantize(Decimal('0.01'))
            ret_islr = (base_en_bs * ret_islr_pct).quantize(Decimal('0.01'))
            ret_municipal = (base_en_bs * ret_mun_pct).quantize(Decimal('0.01'))

            factura.iva = iva.quantize(Decimal('0.01'))
            factura.total_factura = total
            factura.ret_iva = ret_iva
            factura.ret_islr = ret_islr
            factura.porcentaje_ret_municipal = (form.cleaned_data.get('ret_municipal_pct') or form.cleaned_data.get('porcentaje_ret_municipal') or Decimal('0.00'))
            factura.ret_municipal = ret_municipal

            factura.save()
            messages.success(request, "Factura registrada correctamente.")
            # TODO: generar asiento contable automático (integración con contabilidad app)
            return redirect('compras:lista_facturas')
    else:
        form = FacturaForm()
    return render(request, 'compras/facturas/form.html', {'form': form, 'accion': 'Crear Factura'})

def editar_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            factura = form.save(commit=False)

            # recalculos similares a crear
            monto_base = form.cleaned_data.get('monto_base') or Decimal('0.00')
            tasa = form.cleaned_data.get('tasa_cambio') or Decimal('1.00')
            moneda = form.cleaned_data.get('moneda')
            aplica_iva = form.cleaned_data.get('aplica_iva')

            base_en_bs = (monto_base * tasa) if moneda == 'USD' else monto_base
            iva = (base_en_bs * Decimal('0.16')) if aplica_iva else Decimal('0.00')
            total = (base_en_bs + iva).quantize(Decimal('0.01'))

            ret_iva_pct = (form.cleaned_data.get('ret_iva_pct') or Decimal('0.00')) / Decimal('100.00')
            ret_islr_pct = (form.cleaned_data.get('ret_islr_pct') or Decimal('0.00')) / Decimal('100.00')
            ret_mun_pct = (form.cleaned_data.get('ret_municipal_pct') or Decimal('0.00')) / Decimal('100.00')

            ret_iva = (base_en_bs * ret_iva_pct).quantize(Decimal('0.01'))
            ret_islr = (base_en_bs * ret_islr_pct).quantize(Decimal('0.01'))
            ret_municipal = (base_en_bs * ret_mun_pct).quantize(Decimal('0.01'))

            factura.iva = iva.quantize(Decimal('0.01'))
            factura.total_factura = total
            factura.ret_iva = ret_iva
            factura.ret_islr = ret_islr
            factura.porcentaje_ret_municipal = (form.cleaned_data.get('ret_municipal_pct') or form.cleaned_data.get('porcentaje_ret_municipal') or Decimal('0.00'))
            factura.ret_municipal = ret_municipal

            factura.save()
            messages.success(request, "Factura actualizada correctamente.")
            return redirect('compras:lista_facturas')
    else:
        form = FacturaForm(instance=factura)
        # rellenar campos visibles auxiliares con valores del modelo
        form.fields['rif_proveedor'].initial = factura.proveedor.rif if factura.proveedor else ''
        # si el form tiene campos de porcentaje, inicializarlos:
        if 'ret_municipal_pct' in form.fields:
            form.fields['ret_municipal_pct'].initial = factura.porcentaje_ret_municipal
        if 'ret_iva_pct' in form.fields:
            # back-calc percentage only if monto_base > 0
            try:
                pct = (factura.ret_iva / factura.monto_base * 100) if factura.monto_base else 0
            except Exception:
                pct = 0
            form.fields['ret_iva_pct'].initial = pct

    return render(request, 'compras/facturas/form.html', {'form': form, 'accion': 'Editar Factura'})

def eliminar_factura(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        factura.delete()
        messages.success(request, "Factura eliminada correctamente.")
        return redirect('compras:lista_facturas')
    return render(request, 'compras/facturas/confirm_delete.html', {'f': factura})

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField
from decimal import Decimal
from .models import Factura, Proveedor, OrdenCompra



def facturas_pendientes_view(request):

    # --------------------------
    # Filtros desde parámetros GET
    # --------------------------
    proveedor = request.GET.get("proveedor", "").strip()
    rif = request.GET.get("rif", "").strip()
    estado = request.GET.get("estado", "").strip()   # pendiente | vencida | ""

    # facturas = FacturaProveedor.objects.all()

    # Filtro por proveedor (nombre empresa)
    if proveedor:
        facturas = facturas.filter(proveedor__nombre_empresa__icontains=proveedor)

    # Filtro por RIF
    if rif:
        facturas = facturas.filter(proveedor__rif__icontains=rif)

    # --------------------------
    # Determinar vencidas
    # --------------------------
    hoy = timezone.now().date()

    # Annotation para determinar si está vencida
    facturas = facturas.annotate(
        esta_vencida=ExpressionWrapper(
            Q(fecha_vencimiento__lt=hoy),
            output_field=DecimalField(),
        )
    )

    # Filtro de estado
    if estado == "pendiente":
        facturas = facturas.filter(fecha_vencimiento__gte=hoy)
    elif estado == "vencida":
        facturas = facturas.filter(fecha_vencimiento__lt=hoy)

    # --------------------------
    # Cálculo de KPIs
    # --------------------------
    total_pendientes = facturas.count()

    # Totales en Bolívares
    total_bs = facturas.aggregate(
        total=Sum("total_factura")
    )["total"] or Decimal("0.00")

    # Conversión USD si tu modelo ya tiene "total_usd"
    total_usd = facturas.aggregate(
        total=Sum("total_usd")
    )["total"] or Decimal("0.00")

    # Total vencidas real (sobre el queryset filtrado)
    total_vencidas = facturas.filter(fecha_vencimiento__lt=hoy).count()

    # --------------------------
    # Render con contexto completo
    # --------------------------
    context = {
        "facturas": facturas,
        "total_pendientes": total_pendientes,
        "total_bs": total_bs,
        "total_usd": total_usd,
        "total_vencidas": total_vencidas,
    }

    return render(request, "compras/facturas/pendientes.html", context)

