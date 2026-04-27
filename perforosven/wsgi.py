"""
WSGI config for perforosven project.

Este archivo expone la aplicación WSGI (Web Server Gateway Interface),
usada por servidores tradicionales (ej. Gunicorn, uWSGI, Apache mod_wsgi)
para ejecutar el proyecto Django en modo sincrónico.

Más información:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Establece el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perforosven.settings')

# Crea la instancia de aplicación WSGI
application = get_wsgi_application()

