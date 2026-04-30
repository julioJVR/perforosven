from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'departamento',
        'activo',
        'is_staff',
    )

    list_filter = (
        'role',
        'activo',
        'is_staff',
        'is_superuser',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Información Empresarial', {
            'fields': (
                'role',
                'cargo',
                'telefono',
                'departamento',
                'activo',
            )
        }),
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    ordering = ('username',)