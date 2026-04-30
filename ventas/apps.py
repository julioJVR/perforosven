from django.apps import AppConfig
from django.contrib.auth.decorators import login_required
from core.decorators import module_required

@module_required('ventas')

class VentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ventas'
