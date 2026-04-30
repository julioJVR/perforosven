from .models import UserRole, ModulePermission


# ============================================================
# 🔹 OBTENER ROLES ACTIVOS DEL USUARIO
# ============================================================
def get_user_roles(user):
    """
    Retorna los roles activos asignados a un usuario
    """
    if not user.is_authenticated:
        return []

    return UserRole.objects.filter(
        user=user,
        activo=True,
        role__activo=True
    ).select_related('role')


# ============================================================
# 🔹 SUPERADMIN / SUPERUSER TIENE ACCESO TOTAL
# ============================================================
def is_super_admin(user):
    """
    Verifica si el usuario tiene acceso total
    """
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return UserRole.objects.filter(
        user=user,
        activo=True,
        role__nombre__iexact='Super Administrador'
    ).exists()


# ============================================================
# 🔹 VALIDACIÓN GENERAL DE PERMISOS
# ============================================================
def has_module_permission(user, modulo, accion='puede_ver'):
    """
    Verifica permisos específicos por módulo

    accion:
    - puede_ver
    - puede_crear
    - puede_editar
    - puede_eliminar
    - puede_aprobar
    - puede_exportar
    """

    if not user.is_authenticated:
        return False

    # Super admin tiene acceso total
    if is_super_admin(user):
        return True

    user_roles = get_user_roles(user)

    for user_role in user_roles:
        permiso = ModulePermission.objects.filter(
            role=user_role.role,
            modulo=modulo
        ).first()

        if permiso and getattr(permiso, accion, False):
            return True

    return False


# ============================================================
# 🔹 FUNCIONES ESPECÍFICAS
# ============================================================
def puede_ver(user, modulo):
    return has_module_permission(user, modulo, 'puede_ver')


def puede_crear(user, modulo):
    return has_module_permission(user, modulo, 'puede_crear')


def puede_editar(user, modulo):
    return has_module_permission(user, modulo, 'puede_editar')


def puede_eliminar(user, modulo):
    return has_module_permission(user, modulo, 'puede_eliminar')


def puede_aprobar(user, modulo):
    return has_module_permission(user, modulo, 'puede_aprobar')


def puede_exportar(user, modulo):
    return has_module_permission(user, modulo, 'puede_exportar')