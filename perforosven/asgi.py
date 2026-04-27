"""
ASGI config for perforosven project.

Este archivo expone la aplicación ASGI (Asynchronous Server Gateway Interface),
necesaria para ejecutar el proyecto en servidores compatibles con WebSockets
o despliegues asíncronos (ej. Uvicorn, Daphne).

Más información:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Establece la configuración de Django para este entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perforosven.settings')

# Crea la instancia de aplicación ASGI
application = get_asgi_application()
