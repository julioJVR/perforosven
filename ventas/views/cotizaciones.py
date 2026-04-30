from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse

from ventas.models.cotizacion import Cotizacion
from ventas.models.detalle_cotizacion import DetalleCotizacion
from ventas.models import Contrato, PartidaContrato
from django.contrib.auth.decorators import login_required

from ventas.forms.cotizacion_form import (
    CotizacionForm,
    DetalleCotizacionFormSet
)


def cotizaciones_list(request):
    cotizaciones = Cotizacion.objects.all().order_by("-id")
    return render(request, "ventas/cotizaciones/lista.html", {"cotizaciones": cotizaciones})


def cotizacion_create(request):
    cotizacion = Cotizacion()
    form = CotizacionForm(request.POST or None)
    formset = DetalleCotizacionFormSet(request.POST or None, instance=cotizacion)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            cotizacion = form.save()
            formset.instance = cotizacion
            formset.save()
            messages.success(request, "Cotización registrada correctamente.")
            return redirect("ventas:cotizaciones")

    return render(request, "ventas/cotizaciones/form.html", {
        "form": form, "formset": formset
    })


def cotizacion_edit(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    form = CotizacionForm(request.POST or None, instance=cotizacion)
    formset = DetalleCotizacionFormSet(request.POST or None, instance=cotizacion)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Cotización actualizada correctamente.")
            return redirect("ventas:cotizaciones")

    return render(request, "ventas/cotizaciones/form.html", {
        "form": form,
        "formset": formset,
        "editar": True
    })


# --- API JSON para cargar partidas según contrato seleccionado ---
def partidas_por_contrato(request, contrato_id):
    partidas = PartidaContrato.objects.filter(contrato_id=contrato_id)

    data = [
        {
            "id": p.id,
            "descripcion": p.descripcion,
            "monto": float(p.monto)
        }
        for p in partidas
    ]

    return JsonResponse({"partidas": data})


