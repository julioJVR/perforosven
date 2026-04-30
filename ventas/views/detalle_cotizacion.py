from django.shortcuts import render, redirect, get_object_or_404
from ventas.models import Cotizacion, DetalleCotizacion
from ventas.forms import DetalleCotizacionForm
from django.contrib.auth.decorators import login_required

def detalles_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, pk=cotizacion_id)
    detalles = cotizacion.detalles.all()  # gracias al related_name

    return render(request, "ventas/cotizaciones/detalles.html", {
        "cotizacion": cotizacion,
        "detalles": detalles
    })


def detalle_create(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, pk=cotizacion_id)

    if request.method == "POST":
        form = DetalleCotizacionForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.cotizacion = cotizacion
            detalle.save()
            return redirect("ventas:cotizacion_detalles", cotizacion_id=cotizacion.id)
    else:
        form = DetalleCotizacionForm()

    return render(request, "ventas/cotizaciones/detalle_form.html", {
        "form": form,
        "cotizacion": cotizacion
    })


def detalle_edit(request, pk):
    detalle = get_object_or_404(DetalleCotizacion, pk=pk)
    cotizacion = detalle.cotizacion

    if request.method == "POST":
        form = DetalleCotizacionForm(request.POST, instance=detalle)
        if form.is_valid():
            form.save()
            return redirect("ventas:cotizacion_detalles", cotizacion_id=cotizacion.id)
    else:
        form = DetalleCotizacionForm(instance=detalle)

    return render(request, "ventas/cotizaciones/detalle_form.html", {
        "form": form,
        "cotizacion": cotizacion
    })


def detalle_delete(request, pk):
    detalle = get_object_or_404(DetalleCotizacion, pk=pk)
    cotizacion_id = detalle.cotizacion.id
    detalle.delete()

    return redirect("ventas:cotizacion_detalles", cotizacion_id=cotizacion_id)
