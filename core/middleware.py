from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class LoginRequiredMiddleware:
    """
    Middleware que requiere autenticación en todas las vistas
    excepto login, admin, y static files.
    También verifica permisos de acceso a módulos.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Rutas que no requieren autenticación
        self.exempt_urls = [
            reverse('accounts:login'),
            '/admin/login/',
        ]

    def __call__(self, request):
        # No proteger archivos estáticos ni media
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)
        
        # No proteger rutas exentas
        if request.path in self.exempt_urls:
            return self.get_response(request)
        
        # No proteger admin
        if request.path.startswith('/admin/'):
            return self.get_response(request)
        
        # Si no está autenticado, redirigir a login
        if not request.user.is_authenticated:
            return redirect(f"{reverse('accounts:login')}?next={request.path}")
        
        # Verificar permisos de módulo si aplica
        # (Los decoradores manejan esto, pero aquí podemos agregar lógica adicional)
        
        response = self.get_response(request)
        return response