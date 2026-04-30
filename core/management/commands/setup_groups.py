from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Crea los grupos de usuarios y asigna permisos por módulo'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creando grupos y permisos...'))
        
        # Definir los grupos y sus permisos
        grupos_config = {
            'Administrador': {
                'descripcion': 'Acceso total al sistema',
                'permisos': 'all'  # Todos los permisos
            },
            'Contador': {
                'descripcion': 'Acceso al módulo de contabilidad',
                'apps': ['contabilidad']
            },
            'Compras': {
                'descripcion': 'Acceso al módulo de compras',
                'apps': ['compras']
            },
            'Ventas': {
                'descripcion': 'Acceso al módulo de ventas',
                'apps': ['ventas']
            },
            'Consultor': {
                'descripcion': 'Solo lectura en todos los módulos',
                'permisos': 'view'  # Solo permisos de vista
            }
        }
        
        for nombre_grupo, config in grupos_config.items():
            # Crear o obtener el grupo
            grupo, created = Group.objects.get_or_create(name=nombre_grupo)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Grupo creado: {nombre_grupo}'))
            else:
                self.stdout.write(self.style.WARNING(f'○ Grupo ya existe: {nombre_grupo}'))
                # Limpiar permisos existentes
                grupo.permissions.clear()
            
            # Asignar permisos
            if config.get('permisos') == 'all':
                # Administrador: todos los permisos
                all_permissions = Permission.objects.all()
                grupo.permissions.set(all_permissions)
                self.stdout.write(f'  → Asignados todos los permisos ({all_permissions.count()})')
                
            elif config.get('permisos') == 'view':
                # Consultor: solo permisos de lectura
                view_permissions = Permission.objects.filter(codename__startswith='view_')
                grupo.permissions.set(view_permissions)
                self.stdout.write(f'  → Asignados permisos de lectura ({view_permissions.count()})')
                
            elif 'apps' in config:
                # Permisos específicos por app
                permisos = []
                for app_name in config['apps']:
                    # Obtener todos los content types de la app
                    app_permissions = Permission.objects.filter(
                        content_type__app_label=app_name
                    )
                    permisos.extend(app_permissions)
                    self.stdout.write(f'  → App: {app_name} ({app_permissions.count()} permisos)')
                
                grupo.permissions.set(permisos)
        
        self.stdout.write(self.style.SUCCESS('\n✓ Configuración de grupos completada!'))
        self.stdout.write('\nGrupos creados:')
        for grupo in Group.objects.all():
            self.stdout.write(f'  • {grupo.name} ({grupo.permissions.count()} permisos)')