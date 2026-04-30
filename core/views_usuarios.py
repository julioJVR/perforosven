from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.decorators import admin_required
from django.db.models import Q
from django.utils import timezone


@login_required
@admin_required
def lista_usuarios(request):
    """Vista para listar todos los usuarios"""
    # Filtros
    search = request.GET.get('search', '')
    grupo_filter = request.GET.get('grupo', '')
    estado_filter = request.GET.get('estado', '')
    
    usuarios = User.objects.all().prefetch_related('groups')
    
    # Aplicar filtros
    if search:
        usuarios = usuarios.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    if grupo_filter:
        usuarios = usuarios.filter(groups__name=grupo_filter)
    
    if estado_filter == 'activos':
        usuarios = usuarios.filter(is_active=True)
    elif estado_filter == 'inactivos':
        usuarios = usuarios.filter(is_active=False)
    
    # Obtener todos los grupos para el filtro
    grupos = Group.objects.all()
    
    # Estadísticas
    stats = {
        'total': User.objects.count(),
        'activos': User.objects.filter(is_active=True).count(),
        'inactivos': User.objects.filter(is_active=False).count(),
        'administradores': User.objects.filter(groups__name='Administrador').count(),
    }
    
    context = {
        'usuarios': usuarios,
        'grupos': grupos,
        'stats': stats,
        'search': search,
        'grupo_filter': grupo_filter,
        'estado_filter': estado_filter,
    }
    
    return render(request, 'core/usuarios/lista.html', context)


@login_required
@admin_required
def crear_usuario(request):
    """Vista para crear un nuevo usuario"""
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        grupos_ids = request.POST.getlist('grupos')
        
        # Validaciones
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return redirect('core:crear_usuario')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('core:crear_usuario')
        
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('core:crear_usuario')
        
        # Crear usuario
        try:
            usuario = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            
            # Asignar grupos
            if grupos_ids:
                grupos = Group.objects.filter(id__in=grupos_ids)
                usuario.groups.set(grupos)
            
            messages.success(request, f'Usuario {username} creado exitosamente.')
            return redirect('core:lista_usuarios')
            
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')
            return redirect('core:crear_usuario')
    
    # GET request
    grupos = Group.objects.all()
    context = {'grupos': grupos}
    return render(request, 'core/usuarios/crear.html', context)


@login_required
@admin_required
def editar_usuario(request, user_id):
    """Vista para editar un usuario existente"""
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        grupos_ids = request.POST.getlist('grupos')
        is_active = request.POST.get('is_active') == 'on'
        
        # Actualizar usuario
        try:
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.is_active = is_active
            usuario.save()
            
            # Actualizar grupos
            if grupos_ids:
                grupos = Group.objects.filter(id__in=grupos_ids)
                usuario.groups.set(grupos)
            else:
                usuario.groups.clear()
            
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente.')
            return redirect('core:lista_usuarios')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar usuario: {str(e)}')
            return redirect('core:editar_usuario', user_id=user_id)
    
    # GET request
    grupos = Group.objects.all()
    grupos_usuario = usuario.groups.all()
    
    context = {
        'usuario': usuario,
        'grupos': grupos,
        'grupos_usuario': grupos_usuario,
    }
    return render(request, 'core/usuarios/editar.html', context)


@login_required
@admin_required
def cambiar_password(request, user_id):
    """Vista para cambiar contraseña de un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validaciones
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('core:cambiar_password', user_id=user_id)
        
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('core:cambiar_password', user_id=user_id)
        
        # Cambiar contraseña
        try:
            usuario.set_password(password)
            usuario.save()
            messages.success(request, f'Contraseña de {usuario.username} actualizada exitosamente.')
            return redirect('core:lista_usuarios')
        except Exception as e:
            messages.error(request, f'Error al cambiar contraseña: {str(e)}')
            return redirect('core:cambiar_password', user_id=user_id)
    
    context = {'usuario': usuario}
    return render(request, 'core/usuarios/cambiar_password.html', context)


@login_required
@admin_required
def toggle_usuario(request, user_id):
    """Activar/Desactivar usuario"""
    usuario = get_object_or_404(User, id=user_id)
    
    # No permitir desactivar al propio usuario
    if usuario == request.user:
        messages.error(request, 'No puedes desactivar tu propia cuenta.')
        return redirect('core:lista_usuarios')
    
    # Cambiar estado
    usuario.is_active = not usuario.is_active
    usuario.save()
    
    estado = "activado" if usuario.is_active else "desactivado"
    messages.success(request, f'Usuario {usuario.username} {estado} exitosamente.')
    
    return redirect('core:lista_usuarios')


@login_required
@admin_required
def detalle_usuario(request, user_id):
    """Ver detalles de un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    
    # Obtener información adicional
    grupos = usuario.groups.all()
    permisos = usuario.user_permissions.all()
    
    # Última actividad (si tienes un modelo de sesiones o logs)
    last_login = usuario.last_login
    
    context = {
        'usuario': usuario,
        'grupos': grupos,
        'permisos': permisos,
        'last_login': last_login,
    }
    
    return render(request, 'core/usuarios/detalle.html', context)