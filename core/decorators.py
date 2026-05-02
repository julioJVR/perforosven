from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def role_required(*role_names):
    """
    Decorador que verifica si el usuario tiene uno de los roles especificados.
    
    Uso:
        @role_required('admin', 'contabilidad')
        def mi_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Superadmin y Admin siempre tienen acceso
            if request.user.role in ['superadmin', 'admin']:
                return view_func(request, *args, **kwargs)
            
            # Verificar si tiene uno de los roles requeridos
            if request.user.role in role_names:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, 
                    f'No tienes permisos para acceder a esta sección. '
                    f'Se requiere ser: {", ".join(role_names)}'
                )
                return redirect('core:inicio')
        
        return wrapper
    return decorator


def module_required(module_name):
    """
    Decorador que verifica acceso a un módulo específico.
    
    Uso:
        @module_required('compras')
        def lista_proveedores(request):
            ...
    """
    # Mapeo de módulos a roles permitidos
    module_roles = {
        'compras': ['superadmin', 'admin', 'compras'],
        'ventas': ['superadmin', 'admin', 'ventas'],
        'contabilidad': ['superadmin', 'admin', 'contabilidad', 'auditor'],
        'tesoreria': ['superadmin', 'admin', 'tesoreria'],
        'rrhh': ['superadmin', 'admin', 'rrhh'],
        'nomina': ['superadmin', 'admin', 'nomina', 'rrhh'],
        'configuracion': ['superadmin', 'admin'],
    }
    
    allowed_roles = module_roles.get(module_name, ['superadmin', 'admin'])
    
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Verificar permisos del módulo
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # Auditor tiene acceso de lectura a todo (solo vistas GET)
            if request.user.role == 'auditor' and request.method == 'GET':
                return view_func(request, *args, **kwargs)
            
            messages.error(
                request,
                f'No tienes permisos para acceder al módulo de {module_name.capitalize()}.'
            )
            return redirect('core:inicio')
        
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorador que requiere ser Administrador o Super Administrador.
    
    Uso:
        @admin_required
        def configuracion(request):
            ...
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role in ['superadmin', 'admin'] or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(
                request,
                'Solo los Administradores pueden acceder a esta sección.'
            )
            return redirect('core:inicio')
    
    return wrapper