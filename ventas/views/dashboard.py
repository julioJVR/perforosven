from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import module_required

@module_required('ventas')

def dashboard(request):
    return render(request, 'ventas/dashboard.html')
