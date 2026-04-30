from django.utils import timezone
from .models import (
    AuditLog,
    UserRole,
    SecurityPolicy,
)


# ============================================================
# 🔹 OBTENER IP REAL
# ============================================================
def get_client_ip(request):
    """
    Obtiene la IP del cliente considerando proxies
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


# ============================================================
# 🔹 REGISTRAR AUDITORÍA
# ============================================================
def registrar_auditoria(request, accion, modulo, descripcion):
    """
    Registra acciones críticas del sistema
    """

    policy = SecurityPolicy.objects.first()

    # Si no existe política o auditoría deshabilitada
    if policy and not policy.audit_enabled:
        return

    AuditLog.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        accion=accion,
        modulo=modulo,
        descripcion=descripcion,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )


# ============================================================
# 🔹 ASIGNAR ROL A USUARIO
# ============================================================
def asignar_rol_usuario(user, role):
    """
    Asigna un rol a un usuario evitando duplicados
    """

    user_role, created = UserRole.objects.get_or_create(
        user=user,
        role=role,
        defaults={'activo': True}
    )

    if not created and not user_role.activo:
        user_role.activo = True
        user_role.save()

    return user_role


# ============================================================
# 🔹 DESACTIVAR ROL
# ============================================================
def desactivar_rol_usuario(user, role):
    """
    Desactiva rol específico de un usuario
    """

    UserRole.objects.filter(
        user=user,
        role=role
    ).update(activo=False)


# ============================================================
# 🔹 OBTENER POLÍTICA DE SEGURIDAD
# ============================================================
def get_security_policy():
    """
    Obtiene política global de seguridad
    Si no existe, retorna configuración por defecto
    """

    policy = SecurityPolicy.objects.first()

    if not policy:
        policy = SecurityPolicy.objects.create()

    return policy


# ============================================================
# 🔹 VALIDAR EXPIRACIÓN DE CONTRASEÑA (base futura)
# ============================================================
def password_expired(user):
    """
    Base para futura validación de expiración
    Requiere agregar campo password_changed_at en CustomUser
    """

    if not hasattr(user, 'password_changed_at') or not user.password_changed_at:
        return False

    policy = get_security_policy()

    dias = (timezone.now() - user.password_changed_at).days

    return dias >= policy.password_expiry_days