from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def group_required(*group_names):
    """
    Decorador que verifica si el usuario pertenece a uno de los grupos especificados.
    
    Uso:
        @group_required('Administrador', 'Contador')
        def mi_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Administrador siempre tiene acceso
            if request.user.groups.filter(name='Administrador').exists():
                return view_func(request, *args, **kwargs)
            
            # Verificar si pertenece a alguno de los grupos requeridos
            user_groups = request.user.groups.values_list('name', flat=True)
            has_permission = any(group in user_groups for group in group_names)
            
            if has_permission:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, 
                    f'No tienes permisos para acceder a esta sección. '
                    f'Se requiere ser: {", ".join(group_names)}'
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
    # Mapeo de módulos a grupos permitidos
    module_groups = {
        'compras': ['Administrador', 'Compras'],
        'ventas': ['Administrador', 'Ventas'],
        'contabilidad': ['Administrador', 'Contador'],
        'configuracion': ['Administrador'],
    }
    
    allowed_groups = module_groups.get(module_name, ['Administrador'])
    
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Administrador siempre tiene acceso
            if request.user.groups.filter(name='Administrador').exists():
                return view_func(request, *args, **kwargs)
            
            # Consultor tiene acceso de lectura a todo (solo vistas GET)
            if request.user.groups.filter(name='Consultor').exists():
                if request.method == 'GET':
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(
                        request,
                        'Como Consultor solo tienes permisos de lectura.'
                    )
                    return redirect('core:inicio')
            
            # Verificar permisos del módulo
            user_groups = request.user.groups.values_list('name', flat=True)
            has_permission = any(group in user_groups for group in allowed_groups)
            
            if has_permission:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    f'No tienes permisos para acceder al módulo de {module_name.capitalize()}.'
                )
                return redirect('core:inicio')
        
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorador que requiere ser Administrador.
    
    Uso:
        @admin_required
        def configuracion(request):
            ...
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Administrador').exists() or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(
                request,
                'Solo los Administradores pueden acceder a esta sección.'
            )
            return redirect('core:inicio')
    
    return wrapper