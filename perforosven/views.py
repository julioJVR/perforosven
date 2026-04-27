# perforosven/views.py
from django.shortcuts import render

def home(request):
    """
    Vista principal del sistema.
    Desde aquí se podrá acceder a los distintos módulos, como Compras, Ventas, RRHH, etc.
    """
    return render(request, 'core/inicio.html')
