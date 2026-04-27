# 🏢 SIAC Perforosven

**Sistema Integrado Administrativo-Contable** para la gestión empresarial de Perforosven, S.A.

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.1-38B2AC.svg)](https://tailwindcss.com/)

---

## 📋 Descripción

SIAC Perforosven es un sistema ERP modular diseñado específicamente para empresas venezolanas, que integra:

- 🛒 **Gestión de Compras**: Proveedores, órdenes de compra, facturación
- 💰 **Gestión de Ventas**: Clientes, cotizaciones, contratos y facturación
- 📊 **Contabilidad**: Plan de cuentas, asientos contables, reportes financieros
- 🔐 **Administración**: Usuarios, roles y permisos

### ✨ Características Principales

- ✅ Cálculo automático de IVA y retenciones (ISLR, IVA, Municipal)
- ✅ Integración automática de compras/ventas con contabilidad
- ✅ Soporte multi-moneda (VES/USD)
- ✅ Validación de RIF venezolano
- ✅ Importación de plan de cuentas desde Excel
- ✅ API REST para integraciones
- ✅ Interfaz responsive con TailwindCSS

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 15 o superior
- Node.js 18 o superior (para TailwindCSS)
- Git

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/perforosven.git
cd perforosven
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements/development.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Crear base de datos**
```bash
createdb perforosven_db
```

6. **Ejecutar migraciones**
```bash
python manage.py migrate
```

7. **Crear superusuario**
```bash
python manage.py createsuperuser
```

8. **Instalar dependencias de Node.js**
```bash
npm install
```

9. **Compilar TailwindCSS**
```bash
npm run build:css
```

10. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

Visita `http://localhost:8000` en tu navegador.

---

## 🐳 Instalación con Docker

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/perforosven.git
cd perforosven
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con configuraciones de Docker
```

3. **Construir y ejecutar**
```bash
docker-compose up --build
```

4. **Crear superusuario (en otra terminal)**
```bash
docker-compose exec web python manage.py createsuperuser
```

Visita `http://localhost:8000` en tu navegador.

---

## 📁 Estructura del Proyecto

```
perforosven/
├── compras/              # Módulo de compras
│   ├── models.py         # Proveedor, Producto, OrdenCompra, Factura
│   ├── views.py
│   ├── services.py       # Lógica de negocio
│   └── api/              # Endpoints REST
├── ventas/               # Módulo de ventas
│   ├── models/           # Cliente, Cotizacion, Contrato
│   ├── views/
│   └── forms/
├── contabilidad/         # Módulo contable
│   ├── models/           # CuentaContable, AsientoContable
│   ├── repositories/     # Acceso a datos
│   ├── services/         # Lógica contable
│   └── reportes/         # Generación de reportes
├── core/                 # Funcionalidades compartidas
├── templates/            # Templates HTML
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── perforosven/          # Configuración del proyecto
│   └── settings/         # Settings por entorno
├── requirements/         # Dependencias por entorno
└── manage.py
```

---

## 🧪 Testing

Ejecutar suite de tests:
```bash
pytest
```

Con reporte de cobertura:
```bash
pytest --cov=. --cov-report=html
```

Ver reporte:
```bash
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

---

## 🔧 Desarrollo

### Calidad de Código

Formatear código:
```bash
black .
isort .
```

Verificar estilo:
```bash
flake8
```

Type checking:
```bash
mypy .
```

### Compilar TailwindCSS

Modo desarrollo (watch):
```bash
npm run watch:css
```

Modo producción:
```bash
npm run build:css
```

### Pre-commit Hooks

Instalar hooks:
```bash
pre-commit install
```

Ejecutar manualmente:
```bash
pre-commit run --all-files
```

---

## 📚 Documentación de Módulos

### Módulo de Compras

- **Proveedores**: Gestión completa con validación de RIF
- **Productos**: Catálogo con multi-moneda
- **Órdenes de Compra**: Workflow de aprobación
- **Facturas**: Cálculo automático de impuestos y retenciones

### Módulo de Ventas

- **Clientes**: Base de datos de clientes
- **Cotizaciones**: Generación y seguimiento
- **Contratos**: Gestión de contratos y partidas
- **Facturación**: (En desarrollo)

### Módulo de Contabilidad

- **Plan de Cuentas**: Estructura jerárquica
- **Asientos Contables**: Con validación de cuadre
- **Libros**: Mayor Analítico y Diario
- **Estados Financieros**: Balance General y Estado de Resultados

---

## 🔐 Seguridad

- ✅ Variables de entorno para datos sensibles
- ✅ Autenticación requerida en todas las vistas
- ✅ CSRF protection activado
- ✅ Configuración SSL para producción
- ✅ Secrets nunca en el código fuente

### Configuración de Producción

Ver `perforosven/settings/production.py` para:
- `DEBUG = False`
- `ALLOWED_HOSTS` configurado
- `SECURE_SSL_REDIRECT = True`
- Headers de seguridad

---

## 📊 Estado del Proyecto

| Módulo | Estado | Cobertura Tests |
|--------|--------|-----------------|
| Compras | ✅ Completo | 0% |
| Ventas | 🚧 En desarrollo | 0% |
| Contabilidad | ✅ Funcional | 0% |
| Core | ✅ Completo | 0% |

### Roadmap

Ver `Roadmap_SIAC_Perforosven.docx` para el plan detallado de implementación.

**Próximas funcionalidades:**
- [ ] Sistema de facturación de ventas
- [ ] Reportes contables completos
- [ ] Módulo de tesorería
- [ ] Módulo de inventario
- [ ] Dashboard con gráficos
- [ ] Notificaciones por email

---

## 🤝 Contribución

Este es un proyecto interno. Para contribuir:

1. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
2. Commit tus cambios: `git commit -am 'Agregar nueva funcionalidad'`
3. Push a la rama: `git push origin feature/nueva-funcionalidad`
4. Crea un Pull Request

### Estándares de Código

- Seguir PEP 8
- Usar Black para formateo
- Cobertura de tests > 80% para nuevo código
- Documentar funciones y clases

---

## 📝 Licencia

Copyright © 2024 Perforosven, S.A. Todos los derechos reservados.

Este es un proyecto privado. No distribuir sin autorización.

---

## 👥 Equipo

- **Desarrollo**: [Tu Nombre]
- **Análisis**: [Nombre]
- **Testing**: [Nombre]

---

## 📞 Soporte

Para reportar bugs o solicitar features, crear un issue en el repositorio.

**Email**: soporte@perforosven.com  
**Documentación**: [Wiki del proyecto]

---

## 🙏 Agradecimientos

- Django Framework
- TailwindCSS
- PostgreSQL
- Comunidad Python Venezuela

---

**Última actualización**: Abril 2026
