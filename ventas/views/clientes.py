from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.decorators import module_required

from ..models.cliente import Cliente
from ..forms.cliente_form import ClienteForm


@login_required
@module_required('ventas')
def clientes_list(request):
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'ventas/clientes/lista.html', {
        'clientes': clientes
    })


@login_required
@module_required('ventas')
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ventas:clientes')
    else:
        form = ClienteForm()

    return render(request, 'ventas/clientes/form.html', {
        'form': form,
        'titulo': 'Nuevo Cliente'
    })


@login_required
@module_required('ventas')
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('ventas:clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'ventas/clientes/form.html', {
        'form': form,
        'titulo': 'Editar Cliente'
    })