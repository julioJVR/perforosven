# core/decorators.py

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def role_required(*role_names):
    """
    Verifica si el usuario posee uno de los roles indicados.
    Uso:
        @role_required('admin', 'contabilidad')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):

            # Superusuario Django
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Seguridad por atributo role
            user_role = getattr(request.user, "role", None)

            # Superadmin y admin corporativo
            if user_role in ['superadmin', 'admin']:
                return view_func(request, *args, **kwargs)

            # Roles específicos
            if user_role in role_names:
                return view_func(request, *args, **kwargs)

            messages.error(
                request,
                f"No tienes permisos para acceder a esta sección. "
                f"Roles permitidos: {', '.join(role_names)}"
            )
            return redirect('core:inicio')

        return wrapper
    return decorator


def module_required(module_name):
    """
    Controla acceso a módulos específicos del sistema.
    Uso:
        @module_required('ventas')
    """

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

            # Superusuario Django
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            user_role = getattr(request.user, "role", None)

            # Rol permitido
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # Auditor solo lectura
            if user_role == 'auditor' and request.method == 'GET':
                return view_func(request, *args, **kwargs)

            messages.error(
                request,
                f"No tienes permisos para acceder al módulo de {module_name.capitalize()}."
            )
            return redirect('core:inicio')

        return wrapper
    return decorator


def admin_required(view_func):
    """
    Requiere rol Admin / SuperAdmin / Superuser Django
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        user_role = getattr(request.user, "role", None)

        if user_role in ['superadmin', 'admin']:
            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            "Solo administradores pueden acceder a esta sección."
        )
        return redirect('core:inicio')

    return wrapper