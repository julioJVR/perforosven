from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Usuario corporativo principal del sistema SIAC Perforosven
    """

    ROLES = [
        ('superadmin', 'Super Administrador'),
        ('admin', 'Administrador'),
        ('contabilidad', 'Contabilidad'),
        ('compras', 'Compras'),
        ('ventas', 'Ventas'),
        ('tesoreria', 'Tesorería'),
        ('rrhh', 'Recursos Humanos'),
        ('nomina', 'Nómina'),
        ('auditor', 'Auditor'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='ventas',
        verbose_name='Rol'
    )

    cargo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Cargo'
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )

    departamento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Departamento'
    )

    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"