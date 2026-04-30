from django.conf import settings
from django.db import models
from django.utils import timezone


# ============================================================
# 🔹 ROLES EMPRESARIALES
# ============================================================
class Role(models.Model):
    """
    Roles empresariales del sistema:
    Ej: Contabilidad, Compras, Ventas, RRHH
    """

    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del Rol'
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )

    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# ============================================================
# 🔹 PERMISOS POR MÓDULO
# ============================================================
class ModulePermission(models.Model):
    """
    Control granular de permisos por módulo
    """

    MODULOS = [
        ('core', 'Core'),
        ('compras', 'Compras'),
        ('ventas', 'Ventas'),
        ('contabilidad', 'Contabilidad'),
        ('tesoreria', 'Tesorería'),
        ('rrhh', 'Recursos Humanos'),
        ('nomina', 'Nómina'),
        ('configuracion', 'Configuración'),
    ]

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='permisos'
    )

    modulo = models.CharField(
        max_length=50,
        choices=MODULOS
    )

    puede_ver = models.BooleanField(default=False)
    puede_crear = models.BooleanField(default=False)
    puede_editar = models.BooleanField(default=False)
    puede_eliminar = models.BooleanField(default=False)
    puede_aprobar = models.BooleanField(default=False)
    puede_exportar = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Permiso de Módulo'
        verbose_name_plural = 'Permisos de Módulos'
        unique_together = ('role', 'modulo')
        ordering = ['modulo']

    def __str__(self):
        return f"{self.role.nombre} - {self.modulo}"


# ============================================================
# 🔹 ASIGNACIÓN DE ROLES A USUARIOS
# ============================================================
class UserRole(models.Model):
    """
    Relación entre usuarios y roles
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='roles_asignados'
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='usuarios'
    )

    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    activo = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuarios'
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role.nombre}"


# ============================================================
# 🔹 BITÁCORA DE AUDITORÍA
# ============================================================
class AuditLog(models.Model):
    """
    Registro de acciones críticas del sistema
    """

    ACCIONES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('create', 'Creación'),
        ('update', 'Actualización'),
        ('delete', 'Eliminación'),
        ('approve', 'Aprobación'),
        ('export', 'Exportación'),
        ('access_denied', 'Acceso denegado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='auditorias'
    )

    accion = models.CharField(
        max_length=50,
        choices=ACCIONES
    )

    modulo = models.CharField(
        max_length=100
    )

    descripcion = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    fecha = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        verbose_name = 'Bitácora'
        verbose_name_plural = 'Bitácoras'
        ordering = ['-fecha']

    def __str__(self):
        usuario = self.usuario.username if self.usuario else "Sistema"
        return f"{usuario} - {self.accion} - {self.modulo}"


# ============================================================
# 🔹 POLÍTICAS DE SEGURIDAD
# ============================================================
class SecurityPolicy(models.Model):
    """
    Configuración central de políticas de seguridad
    """

    password_min_length = models.PositiveIntegerField(
        default=8,
        verbose_name='Longitud mínima de contraseña'
    )

    session_timeout_minutes = models.PositiveIntegerField(
        default=60,
        verbose_name='Tiempo de sesión (minutos)'
    )

    max_login_attempts = models.PositiveIntegerField(
        default=5,
        verbose_name='Máximo de intentos de login'
    )

    password_expiry_days = models.PositiveIntegerField(
        default=90,
        verbose_name='Expiración de contraseña (días)'
    )

    require_2fa = models.BooleanField(
        default=False,
        verbose_name='Requiere autenticación de dos factores'
    )

    audit_enabled = models.BooleanField(
        default=True,
        verbose_name='Auditoría habilitada'
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Política de Seguridad'
        verbose_name_plural = 'Políticas de Seguridad'

    def __str__(self):
        return "Política General de Seguridad"