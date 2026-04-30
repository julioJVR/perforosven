from django.apps import AppConfig
from django.contrib.auth.decorators import login_required


class VentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ventas'
