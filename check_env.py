import django
import psycopg2
from django.conf import settings
from django.db import connections
import sys

print("🔍 Verificando entorno Django + PostgreSQL...\n")

# Comprobar versión de Django
print(f"Django versión: {django.get_version()}")

# Comprobar conexión a la base de datos
try:
    db_settings = settings.DATABASES['default']
    print(f"\nIntentando conectar a PostgreSQL...")
    print(f"Host: {db_settings['HOST']}")
    print(f"Base de datos: {db_settings['NAME']}")
    print(f"Usuario: {db_settings['USER']}")
    print(f"Puerto: {db_settings['PORT']}\n")

    connection = psycopg2.connect(
        dbname=db_settings['NAME'],
        user=db_settings['USER'],
        password=db_settings['PASSWORD'],
        host=db_settings['HOST'],
        port=db_settings['PORT']
    )
    connection.close()
    print("✅ Conexión a PostgreSQL exitosa.\n")

except Exception as e:
    print("❌ Error de conexión con PostgreSQL:")
    print(e)
    sys.exit(1)

# Comprobar conexión Django ↔ BD
try:
    connections['default'].cursor()
    print("✅ Django puede comunicarse correctamente con la base de datos.\n")
except Exception as e:
    print("❌ Django no puede comunicarse con la base de datos:")
    print(e)
    sys.exit(1)

print("🎉 Todo está correctamente configurado. ¡Puedes iniciar el desarrollo!")
