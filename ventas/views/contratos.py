from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.decorators import module_required



from ventas.models import Contrato, PartidaContrato
from ventas.forms.contrato_form import (
    ContratoForm,
    PartidaContratoFormSet
)

@module_required('ventas')

def contratos_list(request):
    contratos = Contrato.objects.all().order_by("-id")
    return render(request, "ventas/contratos/lista.html", {"contratos": contratos})


def contrato_create(request):
    contrato = Contrato()
    form = ContratoForm(request.POST or None)
    formset = PartidaContratoFormSet(request.POST or None, instance=contrato)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            contrato = form.save()
            formset.instance = contrato
            formset.save()
            messages.success(request, "Contrato registrado correctamente.")
            return redirect("ventas:contratos")

    return render(
        request,
        "ventas/contratos/form.html",
        {"form": form, "formset": formset}
    )


def contrato_edit(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    form = ContratoForm(request.POST or None, instance=contrato)
    formset = PartidaContratoFormSet(request.POST or None, instance=contrato)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Contrato actualizado correctamente.")
            return redirect("ventas:contratos")

    return render(
        request,
        "ventas/contratos/form.html",
        {"form": form, "formset": formset, "editar": True}
    )


def contrato_delete(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    contrato.delete()
    messages.success(request, "Contrato eliminado.")
    return redirect("ventas:contratos")


# === API PARA COTIZACIONES ===
def obtener_partidas_contrato(request, pk):
    """
    API JSON que envía detalles del contrato 
    para usar en cotizaciones.
    """
    contrato = get_object_or_404(Contrato, pk=pk)
    data = [
        {
            "id": p.id,
            "descripcion": p.descripcion,
            "monto": float(p.monto)
        }
        for p in contrato.partidas.all()
    ]
    return JsonResponse({"partidas": data})
