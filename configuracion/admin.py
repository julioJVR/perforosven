from django.contrib import admin
from .models import (
    Role,
    ModulePermission,
    UserRole,
    AuditLog,
    SecurityPolicy
)


# ============================================================
# 🔹 ROLE ADMIN
# ============================================================
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'activo',
        'fecha_creacion',
        'fecha_actualizacion',
    )

    list_filter = (
        'activo',
        'fecha_creacion',
    )

    search_fields = (
        'nombre',
        'descripcion',
    )

    ordering = ('nombre',)


# ============================================================
# 🔹 MODULE PERMISSION ADMIN
# ============================================================
@admin.register(ModulePermission)
class ModulePermissionAdmin(admin.ModelAdmin):
    list_display = (
        'role',
        'modulo',
        'puede_ver',
        'puede_crear',
        'puede_editar',
        'puede_eliminar',
        'puede_aprobar',
        'puede_exportar',
    )

    list_filter = (
        'modulo',
        'role',
    )

    search_fields = (
        'role__nombre',
        'modulo',
    )

    ordering = (
        'role',
        'modulo',
    )


# ============================================================
# 🔹 USER ROLE ADMIN
# ============================================================
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'role',
        'activo',
        'fecha_asignacion',
    )

    list_filter = (
        'activo',
        'role',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'role__nombre',
    )

    ordering = (
        'user',
        'role',
    )


# ============================================================
# 🔹 AUDIT LOG ADMIN
# ============================================================
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'accion',
        'modulo',
        'ip_address',
        'fecha',
    )

    list_filter = (
        'accion',
        'modulo',
        'fecha',
    )

    search_fields = (
        'usuario__username',
        'modulo',
        'descripcion',
        'ip_address',
    )

    ordering = ('-fecha',)

    readonly_fields = (
        'usuario',
        'accion',
        'modulo',
        'descripcion',
        'ip_address',
        'user_agent',
        'fecha',
    )

    def has_add_permission(self, request):
        return False  # Evita crear auditorías manualmente

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superadmin puede eliminar


# ============================================================
# 🔹 SECURITY POLICY ADMIN
# ============================================================
@admin.register(SecurityPolicy)
class SecurityPolicyAdmin(admin.ModelAdmin):
    list_display = (
        'password_min_length',
        'session_timeout_minutes',
        'max_login_attempts',
        'password_expiry_days',
        'require_2fa',
        'audit_enabled',
        'fecha_actualizacion',
    )

    readonly_fields = (
        'fecha_actualizacion',
    )

    def has_add_permission(self, request):
        # Solo permitir una política global
        return not SecurityPolicy.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser