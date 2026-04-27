#!/bin/bash

# Script de Limpieza del Proyecto SIAC Perforosven
# Ejecuta el PASO 0 del Roadmap
# Uso: bash cleanup_project.sh

set -e  # Salir si hay errores

echo "========================================="
echo "  LIMPIEZA DEL PROYECTO PERFOROSVEN"
echo "========================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para confirmación
confirm() {
    read -p "$1 (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        return 1
    fi
    return 0
}

# Verificar que estamos en la raíz del proyecto
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: Este script debe ejecutarse desde la raíz del proyecto (donde está manage.py)${NC}"
    exit 1
fi

echo -e "${YELLOW}⚠️  IMPORTANTE: Este script eliminará archivos. Asegúrate de tener un backup.${NC}"
echo ""

if ! confirm "¿Deseas continuar?"; then
    echo "Operación cancelada."
    exit 0
fi

echo ""
echo "Iniciando limpieza..."
echo ""

# Contador de archivos eliminados
count=0

# 1. Eliminar db.sqlite3
if [ -f "db.sqlite3" ]; then
    echo -e "${GREEN}✓${NC} Eliminando db.sqlite3..."
    rm db.sqlite3
    ((count++))
fi

# 2. Eliminar __pycache__ recursivamente
echo -e "${GREEN}✓${NC} Eliminando carpetas __pycache__..."
pycache_count=$(find . -type d -name '__pycache__' | wc -l)
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
count=$((count + pycache_count))

# 3. Eliminar archivos .pyc
echo -e "${GREEN}✓${NC} Eliminando archivos .pyc..."
pyc_count=$(find . -name '*.pyc' | wc -l)
find . -name '*.pyc' -delete 2>/dev/null || true
count=$((count + pyc_count))

# 4. Eliminar node_modules/
if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓${NC} Eliminando node_modules/..."
    rm -rf node_modules/
    ((count++))
fi

# 5. Eliminar archivos .bak en compras/static/
if [ -d "compras/static" ]; then
    echo -e "${GREEN}✓${NC} Eliminando archivos .bak en compras/static/..."
    bak_count=$(find compras/static -name '*.bak' 2>/dev/null | wc -l)
    find compras/static -name '*.bak' -delete 2>/dev/null || true
    count=$((count + bak_count))
fi

# 6. Eliminar tailwind_watch.bat
if [ -f "tailwind_watch.bat" ]; then
    echo -e "${GREEN}✓${NC} Eliminando tailwind_watch.bat..."
    rm tailwind_watch.bat
    ((count++))
fi

# 7. Eliminar archivos vacíos en ventas/
echo -e "${GREEN}✓${NC} Eliminando archivos vacíos en módulo ventas..."

for file in "ventas/repositories.py" "ventas/services.py" "ventas/views/facturacion.py" "ventas/views/reportes.py" "ventas/models/retencion.py"; do
    if [ -f "$file" ]; then
        # Verificar si el archivo está vacío o solo tiene espacios
        if [ ! -s "$file" ] || [ -z "$(grep -v '^[[:space:]]*$' "$file")" ]; then
            rm "$file"
            ((count++))
        fi
    fi
done

# 8. Eliminar archivos vacíos en contabilidad/
if [ -f "contabilidad/README.txt" ]; then
    echo -e "${GREEN}✓${NC} Eliminando contabilidad/README.txt..."
    rm contabilidad/README.txt
    ((count++))
fi

if [ -f "contabilidad/models/auxiliares.py" ]; then
    if [ ! -s "contabilidad/models/auxiliares.py" ]; then
        rm contabilidad/models/auxiliares.py
        ((count++))
    fi
fi

if [ -f "contabilidad/models/movimientos.py" ]; then
    if [ ! -s "contabilidad/models/movimientos.py" ]; then
        rm contabilidad/models/movimientos.py
        ((count++))
    fi
fi

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  LIMPIEZA COMPLETADA${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "📊 Estadísticas:"
echo "   - Archivos/carpetas eliminados: $count"
echo ""
echo "✨ El proyecto está ahora limpio y listo para comenzar el desarrollo."
echo ""
echo "📝 Próximos pasos:"
echo "   1. Crear .gitignore"
echo "   2. Crear .env.example"
echo "   3. Crear carpeta requirements/"
echo "   4. Inicializar repositorio Git"
echo ""
echo "Consulta el Roadmap para los pasos detallados."
echo ""
