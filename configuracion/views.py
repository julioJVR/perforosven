from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import module_required


@login_required
@module_required('configuracion')
def dashboard(request):
    return render(request, 'configuracion/dashboard.html')